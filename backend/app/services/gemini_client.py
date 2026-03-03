import os
import json
import time
import random
import concurrent.futures
from typing import Any, Dict

from google import genai
from dotenv import load_dotenv

from app.services.prompt_guard import apply_prompt_guard
from app.services.rate_limiter import apply_rate_limit, RateLimitExceeded
from app.services.response_sanitizer import sanitize_response
from app.services.audit_logger import log_clinical_event
from app.services.syndrome_detector import detect_syndrome as regex_detect_syndrome
from app.services.clinical_override import apply_clinical_override
from app.services.risk_engine import compute_clinical_risk

from app.services.alert_rules import generate_alerts
from app.services.alert_logger import log_alerts

from app.domain.syndromes import SYNDROMES


# =====================================================
# CONFIGURAÇÃO DE AMBIENTE
# =====================================================

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY ou GEMINI_API_KEY não encontrada no ambiente")

client = genai.Client(api_key=API_KEY)


# =====================================================
# CONTROLES DE TIMEOUT / RETRY
# =====================================================

GEMINI_TIMEOUT_SECONDS = 12
GEMINI_MAX_RETRIES = 2
GEMINI_BACKOFF_SECONDS = 1.5


# =====================================================
# CIRCUIT BREAKER (local ao processo)
# =====================================================

_CB_FAILURES = 0
_CB_OPEN_UNTIL = 0.0
_CB_FAILURE_THRESHOLD = 3
_CB_OPEN_SECONDS = 60


def _circuit_allow() -> bool:
    return time.time() >= _CB_OPEN_UNTIL


def _circuit_on_success() -> None:
    global _CB_FAILURES
    _CB_FAILURES = 0


def _circuit_on_failure() -> None:
    global _CB_FAILURES, _CB_OPEN_UNTIL
    _CB_FAILURES += 1
    if _CB_FAILURES >= _CB_FAILURE_THRESHOLD:
        _CB_OPEN_UNTIL = time.time() + _CB_OPEN_SECONDS


# =====================================================
# PROMPT HEADER
# =====================================================

PROMPT_HEADER = """
Você é um médico assistente sênior de Pronto-Socorro adulto.

Responda EXCLUSIVAMENTE em JSON, sem texto fora do JSON.

Formato:
{
  "syndrome": "string",
  "questions_needed": ["string"],
  "differentials": [],
  "red_flags": ["string"],
  "recommended_tests": ["string"],
  "educational_management": ["string"],
  "disclaimer": "Conteúdo educacional. Não substitui avaliação clínica.",
  "prompt_version": "string"
}

Caso clínico:
""".strip()


# Prompts por síndrome (pode expandir depois)
PROMPTS = {
    "dor_toracica": PROMPT_HEADER,
    "dispneia": PROMPT_HEADER,
    "sepse": PROMPT_HEADER,
    "avc": PROMPT_HEADER,
    "sincope": PROMPT_HEADER,
    "dor_abdominal": PROMPT_HEADER,
    "trauma": PROMPT_HEADER,
    "intoxicacao": PROMPT_HEADER,
}


# =====================================================
# FALLBACK DETERMINÍSTICO
# =====================================================

def deterministic_fallback(
    syndrome: str,
    prompt_version: str = "fallback"
) -> Dict[str, Any]:
    return {
        "syndrome": syndrome or "indefinido",
        "questions_needed": [
            "Tempo de início e evolução dos sintomas.",
            "Sinais vitais atuais.",
            "Comorbidades e medicações em uso.",
        ],
        "differentials": [],
        "red_flags": [
            "Instabilidade hemodinâmica",
            "Insuficiência respiratória/hipoxemia",
            "Alteração do nível de consciência",
        ],
        "recommended_tests": [
            "Monitorização contínua",
            "Avaliação clínica imediata",
        ],
        "educational_management": [
            "Fallback determinístico. Priorizar abordagem ABCDE e protocolo institucional."
        ],
        "disclaimer": "Conteúdo educacional. Não substitui avaliação clínica.",
        "prompt_version": prompt_version,
    }


# =====================================================
# GEMINI CORE
# =====================================================

def _gemini_generate(prompt: str):
    return client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
    )


def _call_with_timeout(prompt: str, timeout: int):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_gemini_generate, prompt)
        return future.result(timeout=timeout)


def _sleep_backoff(attempt: int):
    delay = GEMINI_BACKOFF_SECONDS * attempt
    delay += random.uniform(0, 0.25)
    time.sleep(delay)


def _call_gemini_with_retry(prompt: str) -> str:
    last_err = None

    for attempt in range(GEMINI_MAX_RETRIES + 1):
        try:
            if not _circuit_allow():
                raise RuntimeError("Circuit breaker ativo")

            resp = _call_with_timeout(prompt, GEMINI_TIMEOUT_SECONDS)
            text = getattr(resp, "text", "").strip()

            if not text:
                raise ValueError("Resposta vazia do modelo")

            _circuit_on_success()
            return text

        except Exception as e:
            last_err = e
            _circuit_on_failure()

            if attempt >= GEMINI_MAX_RETRIES:
                break

            _sleep_backoff(attempt + 1)

    raise last_err or RuntimeError("Falha desconhecida no Gemini")


# =====================================================
# FUNÇÃO PRINCIPAL
# =====================================================

def call_gemini(user_message: str, doctor_id: str) -> Dict[str, Any]:
    start_time = time.time()
    syndrome = "indefinido"

    # Vamos manter um evento canônico mínimo (dict) e evoluir
    event: Dict[str, Any] = {
        "doctor_id": doctor_id,
        "input_message": user_message,
    }

    try:
        # 1) Entrada mínima
        if not user_message or len(user_message.strip()) < 10:
            safe = sanitize_response(
                deterministic_fallback("indefinido", "guard-input")
            )

            risk = compute_clinical_risk(
                syndrome=safe.get("syndrome", "indefinido"),
                red_flags=safe.get("red_flags", []),
                context=None,
            )
            safe["clinical_risk"] = risk

            event.update({
                "syndrome": safe.get("syndrome"),
                "prompt_version": safe.get("prompt_version"),
                "red_flags": safe.get("red_flags", []),
                "clinical_risk": risk,
                "status": "guard_input",
                "latency_ms": int((time.time() - start_time) * 1000),
            })

            # Auditoria + alertas
            log_clinical_event(event)
            alerts = generate_alerts(event)
            log_alerts(alerts, event)

            return safe

        # 2) Guards
        apply_prompt_guard(user_message)
        apply_rate_limit(doctor_id)

        # 3) Síndrome determinística
        detected = regex_detect_syndrome(user_message)
        syndrome = apply_clinical_override(user_message, detected)

        if syndrome not in PROMPTS:
            syndrome = "indefinido"

        # 4) Prompt final
        prompt = PROMPTS.get(syndrome, PROMPT_HEADER) + "\n" + user_message.strip()

        # 5) Gemini
        raw = _call_gemini_with_retry(prompt)
        parsed = json.loads(raw)

        parsed["detected_syndrome"] = syndrome
        parsed["prompt_version"] = parsed.get("prompt_version", "guarded")

        # 6) Sanitização
        safe = sanitize_response(parsed)

        # 7) RISCO CLÍNICO (sempre)
        risk = compute_clinical_risk(
            syndrome=safe.get("syndrome", "indefinido"),
            red_flags=safe.get("red_flags", []),
            context=None,
        )
        safe["clinical_risk"] = risk

        # 8) Evento canônico (auditoria)
        event.update({
            "syndrome": safe.get("syndrome"),
            "prompt_version": safe.get("prompt_version"),
            "red_flags": safe.get("red_flags", []),
            "clinical_risk": risk,
            "status": "success",
            "latency_ms": int((time.time() - start_time) * 1000),
        })

        log_clinical_event(event)

        # 9) Alertas em tempo real
        alerts = generate_alerts(event)
        log_alerts(alerts, event)

        return safe

    except RateLimitExceeded as e:
        safe = sanitize_response(deterministic_fallback("indefinido", "rate-limit"))
        safe["educational_management"] = [str(e)]

        risk = compute_clinical_risk(
            syndrome=safe.get("syndrome", "indefinido"),
            red_flags=safe.get("red_flags", []),
            context=None,
        )
        safe["clinical_risk"] = risk

        event.update({
            "syndrome": safe.get("syndrome"),
            "prompt_version": safe.get("prompt_version"),
            "red_flags": safe.get("red_flags", []),
            "clinical_risk": risk,
            "status": "rate_limited",
            "latency_ms": int((time.time() - start_time) * 1000),
            "error": str(e),
        })

        log_clinical_event(event)
        alerts = generate_alerts(event)
        log_alerts(alerts, event)

        return safe

    except Exception as e:
        safe = sanitize_response(deterministic_fallback(syndrome, "fallback"))

        risk = compute_clinical_risk(
            syndrome=safe.get("syndrome", "indefinido"),
            red_flags=safe.get("red_flags", []),
            context=None,
        )
        safe["clinical_risk"] = risk

        event.update({
            "syndrome": safe.get("syndrome"),
            "prompt_version": safe.get("prompt_version"),
            "red_flags": safe.get("red_flags", []),
            "clinical_risk": risk,
            "status": "error",
            "latency_ms": int((time.time() - start_time) * 1000),
            "error": str(e),
        })

        log_clinical_event(event)
        alerts = generate_alerts(event)
        log_alerts(alerts, event)

        return safe

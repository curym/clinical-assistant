from __future__ import annotations
from typing import Any, Dict, List


def generate_alerts(event: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Recebe o ClinicalAuditEvent serializado (dict) e retorna lista de alertas.
    Cada alerta é um dict simples e serializável.
    """
    alerts: List[Dict[str, Any]] = []

    syndrome = event.get("syndrome", "indefinido")
    risk = (event.get("clinical_risk") or {}).get("level", "indefinido")
    prompt_version = event.get("prompt_version", "") or ""
    is_fallback = (
        prompt_version.startswith("fallback")
        or prompt_version in ["guard-input", "rate-limit", "deterministic-fallback"]
    )
    latency_ms = int(event.get("latency_ms", 0) or 0)

    red_flags = event.get("red_flags") or []
    if not isinstance(red_flags, list):
        red_flags = []

    # 🔴 REGRA 1 — ALTO RISCO + FALLBACK
    if risk == "alto" and is_fallback:
        alerts.append({
            "type": "CRITICAL",
            "rule": "HIGH_RISK_WITH_FALLBACK",
            "message": "Caso de alto risco avaliado em fallback (contingência).",
        })

    # 🔴 REGRA 2 — Síndromes críticas sem red flags documentadas
    if syndrome in ["sepse", "avc", "cauda_equina"] and len(red_flags) == 0:
        alerts.append({
            "type": "SAFETY",
            "rule": "CRITICAL_SYNDROME_NO_REDFLAGS",
            "message": f"{syndrome} sem red flags documentadas.",
        })

    # 🟠 REGRA 3 — Latência elevada (indicador operacional)
    if latency_ms >= 2000:
        alerts.append({
            "type": "PERFORMANCE",
            "rule": "HIGH_LATENCY",
            "message": f"Latência elevada: {latency_ms} ms.",
        })

    # 🟡 REGRA 4 — Indefinido (qualidade de captura)
    if syndrome == "indefinido":
        alerts.append({
            "type": "QUALITY",
            "rule": "INDEFINITE_SYNDROME",
            "message": "Síndrome indefinida — revisar qualidade do input/regex/override.",
        })

    return alerts

import re

# ===============================
# BLINDAGEM CLÍNICA SEMÂNTICA
# ===============================

FORBIDDEN_PATTERNS = [
    r"\badministre\b",
    r"\binicie\b",
    r"\bprescreva\b",
    r"\bdose\b",
    r"\bmg\b",
    r"\bml\b",
    r"\bvia\b",
    r"\bcada\s+\d+\b",
    r"\btratamento definitivo\b",
    r"\bfaça\b",
    r"\bproceda\b",
    r"\bexecute\b",
]

SAFE_REPLACEMENT = (
    "Conteúdo ajustado por segurança clínica. "
    "A decisão final deve ser tomada pelo médico assistente."
)


def _sanitize_text(text: str) -> str:
    if not text:
        return text

    lower = text.lower()

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, lower):
            return SAFE_REPLACEMENT

    return text


def apply_clinical_guard(payload: dict) -> dict:
    """
    Remove linguagem prescritiva, imperativa ou ilegalmente médica
    do payload final, garantindo uso educacional.
    """

    FIELDS_TO_SANITIZE = [
        "questions_needed",
        "red_flags",
        "recommended_tests",
        "educational_management",
    ]

    for field in FIELDS_TO_SANITIZE:
        if field in payload and isinstance(payload[field], list):
            payload[field] = [_sanitize_text(item) for item in payload[field]]

    # Blindagem final obrigatória
    payload["disclaimer"] = "Conteúdo educacional. Não substitui avaliação clínica."

    return payload

import re

FORBIDDEN_PATTERNS = [
    r"\badministre\b",
    r"\binicie\b",
    r"\bprescreva\b",
    r"\bfaça\b",
    r"\bsolicite imediatamente\b",
    r"\bdose\b",
    r"\bmg\b",
    r"\bml\b",
    r"\bvia\b",
    r"\bcada\b \d+\b",
    r"\btratamento\b definitivo\b",
]

SOFT_REPLACEMENTS = {
    "Administração de": "Avaliação da possibilidade de",
    "Iniciar": "Avaliar indicação de",
    "Prescrever": "Considerar",
    "Solicitar": "Avaliar necessidade de",
    "Realizar": "Avaliar realização de",
}


def sanitize_text(text: str) -> str:
    if not text:
        return text

    lowered = text.lower()

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, lowered):
            return (
                "Conteúdo ajustado por segurança clínica. "
                "Reavaliar conduta conforme julgamento médico."
            )

    for src, tgt in SOFT_REPLACEMENTS.items():
        text = text.replace(src, tgt)

    return text


def sanitize_response(payload: dict) -> dict:
    SAFE_FIELDS = [
        "questions_needed",
        "red_flags",
        "recommended_tests",
        "educational_management",
    ]

    for field in SAFE_FIELDS:
        if field in payload and isinstance(payload[field], list):
            payload[field] = [sanitize_text(item) for item in payload[field]]

    # Garantia final
    payload["disclaimer"] = "Conteúdo educacional. Não substitui avaliação clínica."

    return payload

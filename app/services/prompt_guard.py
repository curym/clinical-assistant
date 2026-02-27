import re

# ===============================
# PADRÕES DE PROMPT INJECTION
# ===============================

FORBIDDEN_PATTERNS = [
    r"ignore (all|previous|above) instructions",
    r"forget your role",
    r"you are now",
    r"act as a doctor and prescribe",
    r"prescreva",
    r"prescrição",
    r"dose",
    r"dosagem",
    r"quantos mg",
    r"qual antibiótico",
    r"qual medicamento",
    r"inicie tratamento",
    r"conduta definitiva",
    r"tratamento definitivo",
    r"faça o diagnóstico",
    r"diagnóstico final",
    r"me diga o que fazer",
    r"qual a melhor conduta",
    r"receita médica",
]

# ===============================
# FUNÇÃO DE BLOQUEIO
# ===============================

def violates_prompt_policy(user_message: str) -> bool:
    text = user_message.lower()

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text):
            return True

    return False


def apply_prompt_guard(user_message: str) -> None:
    """
    Lança exceção se houver tentativa de prompt injection
    """
    if violates_prompt_policy(user_message):
        raise ValueError(
            "Solicitação contém tentativa de prescrição, "
            "diagnóstico definitivo ou violação de escopo educacional."
        )

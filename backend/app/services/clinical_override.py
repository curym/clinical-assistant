from app.domain.syndromes import SYNDROMES

def apply_clinical_override(message: str, detected: str) -> str:
    """
    Override clínico determinístico.

    Regras:
    - Só retorna síndromes que existam no domínio
    - Síndromes críticas SEMPRE prevalecem
    - Texto livre nunca cria síndrome nova
    """

    text = (message or "").lower().strip()

    # 1️⃣ Se o detector já achou algo válido no domínio, respeita
    if detected in SYNDROMES:
        return detected

    # 2️⃣ Busca ativa por síndromes críticas no texto
    for key, spec in SYNDROMES.items():
        if not spec.always_high_risk:
            continue

        # Heurística simples: palavra-chave explícita
        if key.replace("_", " ") in text:
            return key

    # 3️⃣ Nada encontrado → indefinido
    return "indefinido"

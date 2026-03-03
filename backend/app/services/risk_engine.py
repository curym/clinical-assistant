from typing import List, Dict, Any

from app.domain.syndromes import SYNDROMES


def compute_clinical_risk(
    syndrome: str,
    red_flags: List[str],
    context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Motor canônico de risco clínico.

    Retorna:
    - level: alto | moderado | baixo
    - color: red | yellow | green
    - label: string humana
    - rationale: explicação clínica resumida
    """

    context = context or {}
    red_flags = red_flags or []

    # 1️⃣ Síndrome fora do domínio
    if syndrome not in SYNDROMES or syndrome == "indefinido":
        return {
            "level": "baixo",
            "color": "green",
            "label": "BAIXO RISCO",
            "rationale": (
                "Queixa inespecífica ou informação insuficiente para "
                "identificação de síndrome de alto risco."
            ),
        }

    spec = SYNDROMES[syndrome]

    # 2️⃣ Síndrome intrinsecamente crítica
    if spec.always_high_risk:
        return {
            "level": "alto",
            "color": "red",
            "label": "ALTO RISCO",
            "rationale": (
                f"A síndrome '{spec.label}' é considerada potencialmente "
                "grave por definição clínica e exige avaliação imediata."
            ),
        }

    # 3️⃣ Red flags presentes
    if red_flags:
        return {
            "level": "alto",
            "color": "red",
            "label": "ALTO RISCO",
            "rationale": (
                "Foram identificados sinais de alerta (red flags) que "
                "aumentam o risco clínico independentemente da síndrome base."
            ),
        }

    # 4️⃣ Síndrome definida, sem red flags
    return {
        "level": "moderado",
        "color": "yellow",
        "label": "RISCO MODERADO",
        "rationale": (
            f"A síndrome '{spec.label}' foi identificada, porém sem "
            "sinais imediatos de instabilidade ou gravidade."
        ),
    }

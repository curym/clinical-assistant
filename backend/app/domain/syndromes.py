from typing import Dict, List, Literal

RiskLevel = Literal["alto", "moderado", "baixo"]

class SyndromeSpec:
    def __init__(
        self,
        key: str,
        label: str,
        default_risk: RiskLevel,
        always_high_risk: bool = False,
        mandatory_red_flags: List[str] | None = None,
    ):
        self.key = key
        self.label = label
        self.default_risk = default_risk
        self.always_high_risk = always_high_risk
        self.mandatory_red_flags = mandatory_red_flags or []


SYNDROMES: Dict[str, SyndromeSpec] = {
    "dor_toracica": SyndromeSpec(
        key="dor_toracica",
        label="Dor torácica",
        default_risk="alto",
        always_high_risk=True,
        mandatory_red_flags=[
            "Dor torácica persistente",
            "Instabilidade hemodinâmica",
            "Irradiação típica",
        ],
    ),
    "dispneia": SyndromeSpec(
        key="dispneia",
        label="Dispneia",
        default_risk="alto",
        always_high_risk=True,
        mandatory_red_flags=[
            "Hipoxemia",
            "Uso de musculatura acessória",
        ],
    ),
    "sepse": SyndromeSpec(
        key="sepse",
        label="Sepse",
        default_risk="alto",
        always_high_risk=True,
    ),
    "avc": SyndromeSpec(
        key="avc",
        label="AVC",
        default_risk="alto",
        always_high_risk=True,
    ),
    "hemorragia": SyndromeSpec(
        key="hemorragia",
        label="Hemorragia",
        default_risk="alto",
        always_high_risk=True,
    ),
    "cauda_equina": SyndromeSpec(
        key="cauda_equina",
        label="Síndrome da cauda equina",
        default_risk="alto",
        always_high_risk=True,
    ),
    "sincope": SyndromeSpec(
        key="sincope",
        label="Síncope",
        default_risk="moderado",
    ),
    "dor_abdominal": SyndromeSpec(
        key="dor_abdominal",
        label="Dor abdominal",
        default_risk="moderado",
    ),
    "trauma": SyndromeSpec(
        key="trauma",
        label="Trauma",
        default_risk="moderado",
    ),
    "intoxicacao": SyndromeSpec(
        key="intoxicacao",
        label="Intoxicação",
        default_risk="moderado",
    ),
    "indefinido": SyndromeSpec(
        key="indefinido",
        label="Queixa inespecífica",
        default_risk="baixo",
    ),
}

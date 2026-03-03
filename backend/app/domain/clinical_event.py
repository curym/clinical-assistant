from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import time


@dataclass
class ClinicalEvent:
    # Identificação
    event_id: str
    timestamp: int

    # Contexto do usuário
    doctor_id: str
    input_mode: str  # free | structured

    # Entrada
    user_message: str
    structured_context: Optional[Dict[str, Any]]

    # Processamento
    detected_syndrome: str
    final_syndrome: str
    prompt_version: str
    fallback_used: bool

    # Resultado clínico
    red_flags: List[str]
    clinical_risk: Dict[str, Any]

    # Metadados técnicos
    latency_ms: int
    status: str  # success | fallback | error

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def now() -> int:
        return int(time.time())

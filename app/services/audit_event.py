from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid


@dataclass
class ClinicalAuditEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp_iso: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    timestamp_unix: int = field(
        default_factory=lambda: int(datetime.now(timezone.utc).timestamp())
    )

    doctor_id: str = ""
    input_mode: Optional[str] = None
    status: str = ""

    syndrome: str = "indefinido"
    detected_syndrome: Optional[str] = None

    risk_level: Optional[str] = None
    risk_color: Optional[str] = None
    risk_label: Optional[str] = None

    prompt_version: Optional[str] = None
    is_fallback: bool = False

    red_flags_count: Optional[int] = None
    latency_ms: Optional[int] = None
    error: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

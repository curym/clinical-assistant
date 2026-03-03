import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def _project_root() -> Path:
    """
    Retorna a raiz do projeto (clinical-assistant-backend),
    assumindo estrutura: app/services/audit_logger.py
    """
    return Path(__file__).resolve().parents[2]


def _audit_dir() -> Path:
    d = _project_root() / "audit_logs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def log_clinical_event(event: Any) -> None:
    """
    Grava um evento canônico em JSONL por dia:
    audit_logs/audit_YYYY-MM-DD.jsonl
    """
    audit_dir = _audit_dir()

    # Normaliza payload
    if is_dataclass(event):
        payload: Dict[str, Any] = asdict(event)
    elif isinstance(event, dict):
        payload = dict(event)
    else:
        payload = {"event": str(event)}

    # timestamp padrão
    payload.setdefault("timestamp_iso", datetime.utcnow().isoformat() + "Z")

    filename = f"audit_{datetime.now().date().isoformat()}.jsonl"
    filepath = audit_dir / filename

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

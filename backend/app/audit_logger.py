import json
import time
from datetime import datetime
from pathlib import Path

AUDIT_DIR = Path("logs")
AUDIT_DIR.mkdir(exist_ok=True)

AUDIT_FILE = AUDIT_DIR / "clinical_audit.log"


def log_clinical_event(event: dict):
    """
    Log estruturado para auditoria clínica.
    Nunca lança exceção (fail-safe).
    """
    try:
        event["timestamp"] = datetime.utcnow().isoformat()

        with AUDIT_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    except Exception:
        # Auditoria NUNCA pode derrubar o sistema
        pass

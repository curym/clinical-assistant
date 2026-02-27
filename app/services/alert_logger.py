import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List


def log_alerts(alerts: List[Dict[str, Any]], event: Dict[str, Any]) -> None:
    """
    Grava alertas em arquivos JSONL diários em /alerts.
    Mantém os alertas desacoplados do audit principal.
    """
    if not alerts:
        return

    base_dir = Path(__file__).resolve().parent.parent.parent  # .../app/services -> .../ (raiz)
    alert_dir = base_dir / "alerts"
    alert_dir.mkdir(exist_ok=True)

    filename = f"alerts_{datetime.now().date()}.jsonl"
    filepath = alert_dir / filename

    record_base = {
        "timestamp": datetime.now().isoformat(),
        "doctor_id": event.get("doctor_id"),
        "syndrome": event.get("syndrome"),
        "clinical_risk": event.get("clinical_risk"),
        "prompt_version": event.get("prompt_version"),
    }

    with open(filepath, "a", encoding="utf-8") as f:
        for alert in alerts:
            row = {**record_base, "alert": alert}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

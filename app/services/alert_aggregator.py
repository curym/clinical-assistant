import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Any, List


def aggregate_alerts(alert_file: Path) -> Dict[str, Any]:
    """
    Lê um arquivo alerts_YYYY-MM-DD.jsonl e gera agregações:
    - total de alertas
    - ranking por tipo/regra
    - ranking por médico
    - cruzamento médico x regra
    """
    total_alerts = 0
    by_rule = Counter()
    by_type = Counter()
    by_doctor = Counter()
    doctor_rule_matrix = defaultdict(Counter)

    with open(alert_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            record = json.loads(line)
            alert = record.get("alert", {})
            doctor_id = record.get("doctor_id", "desconhecido")

            rule = alert.get("rule", "UNKNOWN_RULE")
            a_type = alert.get("type", "UNKNOWN_TYPE")

            total_alerts += 1
            by_rule[rule] += 1
            by_type[a_type] += 1
            by_doctor[doctor_id] += 1
            doctor_rule_matrix[doctor_id][rule] += 1

    return {
        "total_alerts": total_alerts,
        "by_rule": dict(by_rule),
        "by_type": dict(by_type),
        "by_doctor": dict(by_doctor),
        "doctor_rule_matrix": {
            doctor: dict(rules)
            for doctor, rules in doctor_rule_matrix.items()
        },
    }


def write_aggregate(
    aggregate: Dict[str, Any],
    output_file: Path
) -> None:
    output_file.parent.mkdir(exist_ok=True, parents=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(aggregate, f, ensure_ascii=False, indent=2)

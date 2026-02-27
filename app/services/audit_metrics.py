import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _audit_dir() -> Path:
    return _project_root() / "audit_logs"


def _parse_day_from_filename(name: str) -> Optional[date]:
    # audit_YYYY-MM-DD.jsonl
    try:
        if not name.startswith("audit_"):
            return None
        core = name.replace("audit_", "").replace(".jsonl", "")
        return datetime.strptime(core, "%Y-%m-%d").date()
    except Exception:
        return None


def _iter_files(days: int) -> List[Path]:
    audit_dir = _audit_dir()
    if not audit_dir.exists():
        return []

    files = []
    for p in audit_dir.glob("audit_*.jsonl"):
        d = _parse_day_from_filename(p.name)
        if not d:
            continue
        files.append((d, p))

    files.sort(key=lambda x: x[0], reverse=True)

    if days <= 0:
        return [p for _, p in files]

    return [p for _, p in files[:days]]


def _safe_get(d: Dict[str, Any], key: str, default=None):
    v = d.get(key, default)
    return default if v is None else v


def load_events(days: int = 7) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    for file in _iter_files(days):
        try:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        events.append(json.loads(line))
                    except Exception:
                        # ignora linha corrompida
                        continue
        except Exception:
            continue
    return events


def compute_metrics(days: int = 7) -> Dict[str, Any]:
    events = load_events(days=days)

    total = len(events)

    # agregadores
    by_syndrome: Dict[str, int] = {}
    by_risk: Dict[str, int] = {"alto": 0, "moderado": 0, "baixo": 0, "desconhecido": 0}
    by_doctor: Dict[str, int] = {}
    fallback_count = 0
    indefinido_count = 0

    for ev in events:
        doctor_id = str(_safe_get(ev, "doctor_id", "unknown"))
        syndrome = str(_safe_get(ev, "syndrome", "indefinido"))
        prompt_version = str(_safe_get(ev, "prompt_version", ""))

        # risco
        risk = ev.get("clinical_risk") or {}
        risk_level = str(risk.get("level") or "desconhecido")

        # fallback (regra simples e robusta)
        is_fallback = (
            "fallback" in prompt_version
            or prompt_version in ("guard-input", "rate-limit")
            or bool(_safe_get(ev, "is_fallback", False))
        )

        by_doctor[doctor_id] = by_doctor.get(doctor_id, 0) + 1
        by_syndrome[syndrome] = by_syndrome.get(syndrome, 0) + 1

        if syndrome == "indefinido":
            indefinido_count += 1

        if risk_level not in by_risk:
            by_risk["desconhecido"] += 1
        else:
            by_risk[risk_level] += 1

        if is_fallback:
            fallback_count += 1

    def pct(x: int) -> float:
        if total <= 0:
            return 0.0
        return round((x / total) * 100.0, 2)

    # top syndromes
    top_syndromes = sorted(by_syndrome.items(), key=lambda x: x[1], reverse=True)[:10]
    top_doctors = sorted(by_doctor.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "window_days": days,
        "total_events": total,
        "fallback": {
            "count": fallback_count,
            "pct": pct(fallback_count),
        },
        "indefinido": {
            "count": indefinido_count,
            "pct": pct(indefinido_count),
        },
        "risk_distribution": {
            "alto": {"count": by_risk.get("alto", 0), "pct": pct(by_risk.get("alto", 0))},
            "moderado": {"count": by_risk.get("moderado", 0), "pct": pct(by_risk.get("moderado", 0))},
            "baixo": {"count": by_risk.get("baixo", 0), "pct": pct(by_risk.get("baixo", 0))},
            "desconhecido": {"count": by_risk.get("desconhecido", 0), "pct": pct(by_risk.get("desconhecido", 0))},
        },
        "top_syndromes": [{"syndrome": s, "count": c, "pct": pct(c)} for s, c in top_syndromes],
        "top_doctors": [{"doctor_id": d, "count": c, "pct": pct(c)} for d, c in top_doctors],
    }

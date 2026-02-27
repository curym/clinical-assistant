import sys
from pathlib import Path
from datetime import date

from app.services.alert_aggregator import aggregate_alerts, write_aggregate


def main():
    base_dir = Path(__file__).resolve().parent.parent.parent
    alerts_dir = base_dir / "alerts"
    aggregates_dir = alerts_dir / "aggregates"

    # Data opcional via CLI: YYYY-MM-DD
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
    else:
        target_date = date.today().isoformat()

    alert_file = alerts_dir / f"alerts_{target_date}.jsonl"

    if not alert_file.exists():
        print(f"[ERRO] Arquivo não encontrado: {alert_file}")
        sys.exit(1)

    aggregate = aggregate_alerts(alert_file)

    output_file = aggregates_dir / f"alerts_aggregate_{target_date}.json"
    write_aggregate(aggregate, output_file)

    print(f"[OK] Agregado gerado em: {output_file}")
    print(f"Total de alertas: {aggregate['total_alerts']}")


if __name__ == "__main__":
    main()

import argparse
import json
from app.services.audit_metrics import compute_metrics


def main():
    parser = argparse.ArgumentParser(description="Analisa audit_logs (JSONL) e gera métricas.")
    parser.add_argument("--days", type=int, default=7, help="Janela em dias (default=7). Use 0 para todos.")
    args = parser.parse_args()

    metrics = compute_metrics(days=args.days)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

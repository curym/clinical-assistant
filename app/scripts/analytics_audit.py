import json
from pathlib import Path
from collections import Counter, defaultdict
from statistics import mean
import csv

# ================================
# CONFIGURAÇÃO
# ================================

BASE_DIR = Path(__file__).resolve().parent.parent
AUDIT_DIR = BASE_DIR / "audit_logs"
OUTPUT_DIR = BASE_DIR / "analytics_output"

OUTPUT_DIR.mkdir(exist_ok=True)

CSV_FILE = OUTPUT_DIR / "clinical_audit_summary.csv"

# ================================
# LEITURA DOS LOGS
# ================================

events = []

for file in AUDIT_DIR.glob("audit_*.jsonl"):
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

if not events:
    print("❌ Nenhum evento encontrado em audit_logs/")
    exit(1)

print(f"✔ {len(events)} eventos carregados")

# ================================
# MÉTRICAS
# ================================

total_events = len(events)

risk_counter = Counter()
syndrome_counter = Counter()
fallback_counter = Counter()
latencies = []

for e in events:
    # RISCO
    risk = (
        e.get("clinical_risk", {})
        .get("level", "indefinido")
    )
    risk_counter[risk] += 1

    # SÍNDROME
    syndrome_counter[e.get("syndrome", "indefinido")] += 1

    # FALLBACK
    if e.get("prompt_version", "").startswith("fallback"):
        fallback_counter["fallback"] += 1

    # LATÊNCIA
    if "latency_ms" in e:
        latencies.append(e["latency_ms"])

# ================================
# ESTATÍSTICAS
# ================================

avg_latency = round(mean(latencies), 1) if latencies else 0
p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0

# ================================
# PRINT NO TERMINAL
# ================================

print("\n===== RESUMO CLÍNICO =====")
print(f"Total de atendimentos: {total_events}")
print(f"Alto risco: {risk_counter.get('alto', 0)}")
print(f"Risco moderado: {risk_counter.get('moderado', 0)}")
print(f"Baixo risco: {risk_counter.get('baixo', 0)}")
print(f"Fallbacks: {fallback_counter.get('fallback', 0)}")

print("\n===== TOP SÍNDROMES =====")
for s, c in syndrome_counter.most_common(10):
    print(f"{s}: {c}")

print("\n===== PERFORMANCE =====")
print(f"Latência média (ms): {avg_latency}")
print(f"Latência p95 (ms): {p95_latency}")

# ================================
# CSV (EXCEL / BI)
# ================================

with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Métrica", "Valor"])

    writer.writerow(["Total de atendimentos", total_events])
    writer.writerow(["Alto risco", risk_counter.get("alto", 0)])
    writer.writerow(["Risco moderado", risk_counter.get("moderado", 0)])
    writer.writerow(["Baixo risco", risk_counter.get("baixo", 0)])
    writer.writerow(["Fallbacks", fallback_counter.get("fallback", 0)])
    writer.writerow(["Latência média (ms)", avg_latency])
    writer.writerow(["Latência p95 (ms)", p95_latency])

    writer.writerow([])
    writer.writerow(["Síndrome", "Quantidade"])

    for s, c in syndrome_counter.items():
        writer.writerow([s, c])

print(f"\n📁 CSV gerado em: {CSV_FILE}")

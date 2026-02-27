import time
from collections import defaultdict, deque

# ===============================
# CONFIGURAÇÃO
# ===============================

MAX_REQUESTS_PER_MINUTE = 5
COOLDOWN_SECONDS = 5

# ===============================
# ESTRUTURAS EM MEMÓRIA
# ===============================

request_log = defaultdict(deque)
last_request_time = {}

# ===============================
# EXCEÇÃO DEDICADA
# ===============================

class RateLimitExceeded(Exception):
    pass

# ===============================
# FUNÇÃO PRINCIPAL
# ===============================

def apply_rate_limit(doctor_id: str):
    now = time.time()

    # -------------------------------
    # Cooldown simples
    # -------------------------------
    last_time = last_request_time.get(doctor_id)
    if last_time and (now - last_time) < COOLDOWN_SECONDS:
        raise RateLimitExceeded(
            f"Aguarde {COOLDOWN_SECONDS} segundos entre consultas."
        )

    last_request_time[doctor_id] = now

    # -------------------------------
    # Janela deslizante de 60s
    # -------------------------------
    window = request_log[doctor_id]

    # Remove requisições antigas
    while window and (now - window[0]) > 60:
        window.popleft()

    if len(window) >= MAX_REQUESTS_PER_MINUTE:
        raise RateLimitExceeded(
            "Limite de consultas por minuto excedido."
        )

    window.append(now)

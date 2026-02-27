import re

PATTERNS = {
    "dor_toracica": [
        r"dor torácica", r"dor no peito", r"opressiva",
        r"precordial", r"irradia", r"braço esquerdo",
        r"sudorese", r"náusea", r"angina"
    ],
    "dispneia": [
        r"dispneia", r"falta de ar", r"hipoxemia",
        r"satur", r"sp[o0]2"
    ],
    "sepse": [
        r"febre", r"hipotens", r"taquicard",
        r"confusão", r"infecção"
    ],
    "avc": [
        r"fraqueza", r"afasia", r"hemiparesia",
        r"avc", r"neurológ"
    ],
    "trauma": [
        r"acidente", r"trauma", r"fratura", r"contusão"
    ],
    "sincope": [
        r"síncope", r"desmaio", r"lipotimia"
    ],
    "dor_abdominal": [
        r"dor abdominal", r"epigástr", r"abdome",
        r"vômito"
    ],
    "intoxicacao": [
        r"overdose", r"intoxica", r"ingestão",
        r"substância"
    ],
}

PRIORITY = [
    "dor_toracica",
    "avc",
    "sepse",
    "dispneia",
    "trauma",
    "sincope",
    "dor_abdominal",
    "intoxicacao",
]

def score_syndromes(message: str) -> dict:
    text = message.lower()
    scores = {}

    for syndrome, patterns in PATTERNS.items():
        scores[syndrome] = sum(
            1 for p in patterns if re.search(p, text)
        )

    return scores

def detect_syndrome(message: str) -> str:
    scores = score_syndromes(message)

    for syndrome in PRIORITY:
        if scores.get(syndrome, 0) >= 2:
            return syndrome

    return "indefinido"

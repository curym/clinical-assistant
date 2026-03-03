def route_syndrome(text: str) -> str:
    t = text.lower()

    if any(x in t for x in ["dor torácica", "peito", "precordial"]):
        return "dor_toracica"
    if any(x in t for x in ["dispneia", "falta de ar", "dispnéia"]):
        return "dispneia"
    if any(x in t for x in ["dor abdominal", "abdome"]):
        return "dor_abdominal"
    if any(x in t for x in ["febre", "sepse", "calafrio"]):
        return "sepse"
    if any(x in t for x in ["avc", "déficit neurológico", "fala arrastada"]):
        return "avc"
    if any(x in t for x in ["hipertensão", "pa elevada", "crise hipertensiva"]):
        return "crise_hipertensiva"

    return "indefinido"

import pytest
from app.services.syndrome_detector import detect_syndrome

@pytest.mark.parametrize(
    "message,expected",
    [
        # Dor torácica
        ("Paciente com dor torácica opressiva há 40 minutos", "dor_toracica"),
        ("Dor no peito irradiando para braço esquerdo", "dor_toracica"),

        # Dispneia
        ("Paciente com falta de ar súbita, SpO2 88%", "dispneia"),
        ("Dispneia progressiva e hipoxemia", "dispneia"),

        # Sepse
        ("Paciente com febre alta e calafrios", "sepse"),
        ("Hipotensão, taquicardia e suspeita de infecção", "sepse"),

        # AVC
        ("Fraqueza súbita em hemicorpo direito", "avc"),
        ("Afasia de início agudo", "avc"),

        # Síncope
        ("Paciente apresentou síncope ao levantar", "sincope"),
        ("Desmaio seguido de queda", "sincope"),

        # Dor abdominal
        ("Dor abdominal intensa em epigástrio", "dor_abdominal"),
        ("Náuseas, vômitos e dor em abdome", "dor_abdominal"),

        # Trauma
        ("Paciente vítima de queda da própria altura", "trauma"),
        ("Acidente automobilístico com trauma torácico", "trauma"),

        # Intoxicação
        ("Suspeita de overdose medicamentosa", "intoxicacao"),
        ("Ingestão de substância desconhecida", "intoxicacao"),

        # Indefinido
        ("asdfghjkl", "indefinido"),
        ("Paciente relata mal-estar inespecífico", "indefinido"),
    ]
)
def test_detect_syndrome(message, expected):
    assert detect_syndrome(message) == expected

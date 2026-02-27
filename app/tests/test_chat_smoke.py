from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def post(msg: str):
    return client.post(
        "/chat",
        json={"doctor_id": "teste", "message": msg, "context": None},
    )

def test_chat_vago_nao_quebra():
    r = post("tosse seca")
    assert r.status_code == 200
    data = r.json()
    assert "syndrome" in data

def test_chat_dor_toracica_alto_risco():
    r = post("dor torácica opressiva há 40 minutos, PA 80x50, sudorese fria")
    assert r.status_code == 200
    data = r.json()
    assert data.get("syndrome") in ["dor_toracica", "dispneia", "sepse", "avc", "indefinido", "outra"]

def test_chat_dispneia_spo2_baixa():
    r = post("falta de ar súbita, SpO2 88%")
    assert r.status_code == 200
    data = r.json()
    assert data.get("syndrome") in ["dispneia", "indefinido", "outra"]

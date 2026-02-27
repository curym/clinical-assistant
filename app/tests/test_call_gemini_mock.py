import json
from unittest.mock import patch
from app.services.gemini_client import call_gemini


def load_mock_response():
    with open("app/tests/mocks/gemini_success.json", encoding="utf-8") as f:
        return f.read()


@patch("app.services.gemini_client._call_gemini_with_retry")
def test_call_gemini_success(mock_gemini):
    # Arrange
    mock_gemini.return_value = load_mock_response()

    message = "Paciente com dor torácica opressiva há 40 minutos"
    doctor_id = "doctor_test"

    # Act
    result = call_gemini(
        user_message=message,
        doctor_id=doctor_id
    )

    # Assert
    assert result["syndrome"] == "dor_toracica"
    assert "ECG" in " ".join(result["recommended_tests"])
    assert result["prompt_version"] == "mock"
    assert result["disclaimer"].startswith("Conteúdo educacional")

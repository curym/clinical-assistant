import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.gemini_client import call_gemini
from app.services.audit_metrics import compute_metrics

load_dotenv()

app = FastAPI(title="Clinical Assistant Backend")


# CORS (dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    doctor_id: str
    message: str
    context: Optional[Dict[str, Any]] = None
    input_mode: Optional[str] = None


@app.post("/chat")
def chat(payload: ChatRequest) -> Dict[str, Any]:
    # O backend (gemini_client) já faz guards e log do audit_event
    return call_gemini(user_message=payload.message, doctor_id=payload.doctor_id)


@app.get("/internal/metrics")
def internal_metrics(
    days: int = 7,
    x_internal_key: Optional[str] = Header(default=None),
) -> Dict[str, Any]:
    """
    Endpoint interno (não expor em produção sem auth de verdade).
    Proteção simples por header:
      X-Internal-Key: <INTERNAL_API_KEY>

    Configure no .env:
      INTERNAL_API_KEY=alguma-chave
    """
    expected = os.getenv("INTERNAL_API_KEY", "").strip()
    if not expected:
        raise HTTPException(status_code=500, detail="INTERNAL_API_KEY não configurada no ambiente")

    if not x_internal_key or x_internal_key.strip() != expected:
        raise HTTPException(status_code=401, detail="Não autorizado")

    return compute_metrics(days=days)

from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    doctor_id: str
    message: str
    context: Optional[dict] = None

class Differential(BaseModel):
    name: str
    reasoning: Optional[str] = None

class ChatResponse(BaseModel):
    syndrome: str
    questions_needed: List[str]
    differentials: List[Differential]
    red_flags: List[str]
    recommended_tests: List[str]
    educational_management: List[str]
    disclaimer: str
    prompt_version: str

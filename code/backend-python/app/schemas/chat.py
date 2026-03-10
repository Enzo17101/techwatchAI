from pydantic import BaseModel

class ChatRequest(BaseModel):
    """Schema for incoming user chat queries."""
    question: str
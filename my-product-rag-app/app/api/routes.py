from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag_service import RAGService

router = APIRouter()

rag_service = RAGService()

#Request / Response Models

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

# Health Check

@router.get('/health')
def health_check():
    return{'status': 'ok'}

#Chat Endponts

@router.post('/chat',response_model=ChatResponse)
def chat(request:ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    answer = rag_service.answer(request.question)

    return{'answer': answer}

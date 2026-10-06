from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.rag_service import RAGService


router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"]
)


rag_service = RAGService()


class ChatRequest(BaseModel):
    message: str


@router.post("")
def chat(request: ChatRequest):

    if not request.message.strip():
        return {
            "message": request.message,
            "answer": (
                "Please enter a question about the "
                "knowledge base."
            ),
            "sources": [],
            "confidence": 0.0,
        }

    result = rag_service.ask(
        request.message
    )

    return {
        "message": request.message,
        "answer": result["answer"],
        "sources": result["sources"],
        "confidence": result["confidence"],
    }
from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.router import AIRequestRouter
from app.rag.rag_service import RAGService
from app.database import tickets_collection
from app.servicenow.client import ServiceNowClient


router = APIRouter(prefix="/tickets", tags=["Tickets"])

ai_router = AIRequestRouter()
rag_service = RAGService()
servicenow = ServiceNowClient()


class TicketRequest(BaseModel):
    message: str


@router.post("/intake")
def intelligent_ticket_intake(request: TicketRequest):

    # Step 1: AI analyzes the employee request
    analysis = ai_router.classify(request.message)

    # Step 2: Search approved knowledge
    rag_result = rag_service.ask(request.message)

    # Step 3: Build ticket record
    ticket = {
        "description": request.message,
        "intent": analysis["intent"],
        "category": analysis["category"],
        "subcategory": analysis["subcategory"],
        "priority": analysis["priority"],
        "impact": analysis["impact"],
        "urgency": analysis["urgency"],
        "assignment_group": analysis["assignment_group"],
        "summary": analysis["summary"],
        "ai_confidence": analysis["confidence"],
        "automation_candidate": analysis["automation_candidate"],
        "status": "Open",
        "knowledge_sources": rag_result["sources"],
    }

    # Step 4: Create ServiceNow incident for incidents
    servicenow_result = None

    if analysis["intent"] == "Incident":
        servicenow_result = servicenow.create_incident(ticket)

        ticket["servicenow_reference"] = servicenow_result["number"]

    # Step 5: Store ticket in MongoDB
    result = tickets_collection.insert_one(ticket)

    return {
        "ticket_id": str(result.inserted_id),
        "request": request.message,
        "analysis": analysis,
        "suggested_resolution": rag_result["answer"],
        "knowledge_sources": rag_result["sources"],
        "servicenow": servicenow_result,
    }
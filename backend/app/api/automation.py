from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from app.automation.agent import SelfHealAgent
from app.database import automation_collection, audit_collection
from app.servicenow.client import ServiceNowClient


router = APIRouter(
    prefix="/automation",
    tags=["Automation"]
)

agent = SelfHealAgent()
servicenow = ServiceNowClient()


class AutomationRequest(BaseModel):
    message: str
    ticket_id: str | None = None


@router.post("/self-heal")
def self_heal(request: AutomationRequest):

    # ---------------------------------------------------------
    # 1. Run the self-healing workflow
    # ---------------------------------------------------------
    result = agent.handle(
        request.message,
        request.ticket_id
    )

    automation = result.get("automation", {})

    # ---------------------------------------------------------
    # 2. Update ServiceNow when automation successfully resolves
    # ---------------------------------------------------------
    servicenow_result = None

    if request.ticket_id and result["status"] == "resolved":

        servicenow_result = servicenow.update_incident(
            request.ticket_id,
            {
                "state": "Resolved",
                "resolution": result["message"],
            }
        )

    # ---------------------------------------------------------
    # 3. Store automation execution in MongoDB
    # ---------------------------------------------------------
    automation_record = {
        "ticket_id": request.ticket_id,
        "request": request.message,
        "action": automation.get("action"),

        "status": (
            automation.get("execution", {}).get("status")
            if automation.get("execution")
            else automation.get("status", "not_available")
        ),

        "result": automation.get("execution"),

        "validation": automation.get("validation"),

        "servicenow": servicenow_result,

        "created_at": datetime.now(timezone.utc),
    }

    automation_insert = automation_collection.insert_one(
        automation_record
    )

    # ---------------------------------------------------------
    # 4. Store audit log
    # ---------------------------------------------------------
    audit_record = {
        "ticket_id": request.ticket_id,

        "actor": "AI Self-Heal Agent",

        "action": automation.get("action"),

        "result": result["status"],

        "message": result["message"],

        "servicenow_reference": (
            servicenow_result.get("number")
            if servicenow_result
            else None
        ),

        "timestamp": datetime.now(timezone.utc),
    }

    audit_insert = audit_collection.insert_one(
        audit_record
    )

    # ---------------------------------------------------------
    # 5. Return complete workflow result
    # ---------------------------------------------------------
    return {
        "status": result["status"],

        "message": result["message"],

        "workflow": result["workflow"],

        "knowledge": result["knowledge"],

        "automation": result["automation"],

        "servicenow": servicenow_result,

        "audit": {
            "automation_id": str(
                automation_insert.inserted_id
            ),

            "audit_id": str(
                audit_insert.inserted_id
            ),
        },
    }
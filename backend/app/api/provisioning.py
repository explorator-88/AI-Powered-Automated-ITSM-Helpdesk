from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.router import AIRequestRouter
from app.database import software_collection, audit_collection
from app.provisioning.catalogue import find_software
from app.provisioning.provisioner import provision_software
from app.servicenow.client import ServiceNowClient


router = APIRouter(prefix="/provisioning", tags=["Provisioning"])

ai_router = AIRequestRouter()
servicenow = ServiceNowClient()


class ProvisioningRequest(BaseModel):
    message: str
    username: str = "employee"


@router.post("/request")
def request_software(request: ProvisioningRequest):

    analysis = ai_router.classify(request.message)

    software = find_software(request.message)

    if software is None:
        return {
            "status": "rejected",
            "message": "The requested software was not found in the approved software catalogue.",
            "analysis": analysis,
        }

    if not software["approved"]:
        return {
            "status": "rejected",
            "message": "The requested software is not approved.",
            "software": software,
        }

    servicenow_result = servicenow.create_request({
        "username": request.username,
        "software": software["name"],
        "category": software["category"],
        "description": request.message,
    })

    provisioning_result = provision_software(
        software["name"],
        request.username,
    )

    software_record = {
        "username": request.username,
        "software": software["name"],
        "software_id": software["software_id"],
        "category": software["category"],
        "status": provisioning_result["status"],
        "servicenow_reference": servicenow_result["number"],
        "created_at": datetime.now(timezone.utc),
    }

    db_result = software_collection.insert_one(software_record)

    audit_record = {
        "actor": "AI Provisioning Agent",
        "action": "software_provisioning",
        "target": software["name"],
        "result": provisioning_result["status"],
        "servicenow_reference": servicenow_result["number"],
        "timestamp": datetime.now(timezone.utc),
    }

    audit_result = audit_collection.insert_one(audit_record)

    return {
        "status": provisioning_result["status"],
        "message": "Software request processed successfully.",
        "software": software,
        "servicenow": servicenow_result,
        "provisioning": provisioning_result,
        "database_id": str(db_result.inserted_id),
        "audit_id": str(audit_result.inserted_id),
    }
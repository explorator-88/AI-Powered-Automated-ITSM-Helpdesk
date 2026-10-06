from fastapi import APIRouter

from app.database import (
    tickets_collection,
    automation_collection,
    software_collection,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def get_dashboard_stats():

    total_tickets = tickets_collection.count_documents({})

    open_tickets = tickets_collection.count_documents({
        "status": "Open"
    })

    resolved_tickets = tickets_collection.count_documents({
        "status": "Resolved"
    })

    escalated_tickets = tickets_collection.count_documents({
        "status": "Escalated"
    })

    software_requests = software_collection.count_documents({})

    # Successful controlled self-healing automations
    successful_automations = automation_collection.count_documents({
        "status": "success"
    })

    total_automations = automation_collection.count_documents({})

    automation_success_rate = (
        round(
            (successful_automations / total_automations) * 100
        )
        if total_automations > 0
        else 0
    )

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
        "escalated_tickets": escalated_tickets,
        "software_requests": software_requests,

        # AI/self-healing resolution metric
        "ai_resolved": successful_automations,

        "successful_automations": successful_automations,
        "total_automations": total_automations,
        "automation_success_rate": automation_success_rate,
    }
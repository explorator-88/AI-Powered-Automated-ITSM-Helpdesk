from fastapi import APIRouter

from app.database import tickets_collection

router = APIRouter()


@router.post("/test-ticket")
def create_test_ticket():
    ticket = {
        "summary": "Test VPN issue",
        "description": "User cannot connect to VPN",
        "category": "Network",
        "subcategory": "VPN",
        "priority": "P2",
        "status": "Open",
    }

    result = tickets_collection.insert_one(ticket)

    return {
        "message": "Ticket created successfully",
        "id": str(result.inserted_id),
    }
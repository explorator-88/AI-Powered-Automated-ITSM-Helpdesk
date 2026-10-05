from datetime import datetime


class MockServiceNow:

    def __init__(self):
        self.incident_counter = 1000
        self.request_counter = 1200

    def create_incident(self, ticket: dict) -> dict:

        self.incident_counter += 1

        number = f"INC{self.incident_counter}"

        return {
            "number": number,
            "sys_id": f"mock-sys-{self.incident_counter}",
            "state": "Open",
            "created_at": datetime.utcnow().isoformat(),
            "message": "Mock ServiceNow incident created successfully",
        }

    def get_incident(self, incident_number: str) -> dict:

        return {
            "number": incident_number,
            "state": "Open",
            "message": "Mock ServiceNow incident retrieved successfully",
        }

    def update_incident(
        self,
        incident_number: str,
        updates: dict
    ) -> dict:

        return {
            "number": incident_number,
            "state": updates.get("state", "Open"),
            "updates": updates,
            "message": "Mock ServiceNow incident updated successfully",
        }

    def create_request(self, request: dict) -> dict:

        self.request_counter += 1

        number = f"REQ{self.request_counter}"

        return {
            "number": number,
            "sys_id": f"mock-req-{self.request_counter}",
            "state": "Requested",
            "created_at": datetime.utcnow().isoformat(),
            "message": "Mock ServiceNow request created successfully",
        }
import os

from app.servicenow.mock import MockServiceNow


class ServiceNowClient:

    def __init__(self):

        mode = os.getenv(
            "SERVICENOW_MODE",
            "mock"
        ).lower()

        self.mode = mode

        if self.mode == "mock":
            self.client = MockServiceNow()
        else:
            raise NotImplementedError(
                "Real ServiceNow integration will be added later."
            )

    def create_incident(self, ticket: dict) -> dict:

        return self.client.create_incident(ticket)

    def get_incident(self, incident_number: str) -> dict:

        return self.client.get_incident(
            incident_number
        )

    def update_incident(
        self,
        incident_number: str,
        updates: dict
    ) -> dict:

        return self.client.update_incident(
            incident_number,
            updates
        )

    def create_request(self, request: dict) -> dict:

        return self.client.create_request(request)
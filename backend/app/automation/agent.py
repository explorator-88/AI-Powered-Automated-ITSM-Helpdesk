from datetime import datetime, timezone

from app.automation.actions import execute_action
from app.rag.rag_service import RAGService


class SelfHealAgent:

    def __init__(self):
        self.rag_service = RAGService()

    def handle(self, message: str, ticket_id: str | None = None) -> dict:
        """
        Execute a controlled self-healing workflow.

        Workflow:
        Identify → Diagnose → Knowledge Search →
        Determine Automation → Execute → Validate
        """

        # 1. Identify
        identification = {
            "request": message,
            "ticket_id": ticket_id,
        }

        # 2. Knowledge search
        rag_result = self.rag_service.ask(message)

        # 3. Determine approved automation
        action_name = self._determine_action(message)

        if action_name is None:
            return {
                "status": "escalated",
                "workflow": identification,
                "knowledge": rag_result,
                "automation": {
                    "action": None,
                    "status": "not_available",
                },
                "message": "No approved self-healing action is available. Escalating to IT helpdesk.",
            }

        # 4. Execute controlled action
        execution_result = execute_action(
            action_name,
            username="employee",
        )

        # 5. Validate
        validation = self._validate(execution_result)

        return {
            "status": "resolved" if validation["success"] else "escalated",
            "workflow": identification,
            "knowledge": rag_result,
            "automation": {
                "action": action_name,
                "execution": execution_result,
                "validation": validation,
            },
            "message": (
                "Issue was successfully resolved using an approved "
                "self-healing automation."
                if validation["success"]
                else "Automation did not resolve the issue. Escalating to IT helpdesk."
            ),
        }

    def _determine_action(self, message: str) -> str | None:
        text = message.lower()

        if "password expired" in text or "password has expired" in text:
            return "password_reset"

        if "account locked" in text or "account is locked" in text:
            return "account_unlock"

        if "outlook" in text and (
            "not syncing" in text
            or "synchronization" in text
            or "sync" in text
        ):
            return "restart_outlook"

        if "vpn" in text and (
            "status" in text
            or "available" in text
            or "down" in text
        ):
            return "vpn_status_check"

        return None

    def _validate(self, execution_result: dict) -> dict:
        success = execution_result.get("status") == "success"

        return {
            "success": success,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "result": (
                "Automation completed successfully."
                if success
                else "Automation failed."
            ),
        }
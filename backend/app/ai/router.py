from typing import Any


class AIRequestRouter:

    def classify(self, message: str) -> dict[str, Any]:

        text = message.lower().strip()

        # ---------------------------------------------------------
        # 1. PASSWORD / ACCOUNT AUTOMATION
        # ---------------------------------------------------------
        password_keywords = [
            "password expired",
            "password has expired",
            "password reset",
            "forgot my password",
            "forgot password",
            "cannot login",
            "can't login",
            "cannot log in",
            "can't log in",
            "account locked",
            "account unlock",
        ]

        if any(keyword in text for keyword in password_keywords):

            return {
                "intent": "Automatable Issue",
                "category": "Account and Access",
                "subcategory": "Password",
                "priority": "P2",
                "impact": "Individual",
                "urgency": "High",
                "assignment_group": "Identity and Access Management",
                "summary": "Password or account access issue",
                "automation_candidate": True,
                "confidence": 0.96,
            }

        # ---------------------------------------------------------
        # 2. APPLICATION ACCESS
        # ---------------------------------------------------------
        access_keywords = [
            "application access",
            "access to application",
            "access request",
            "cannot access application",
            "can't access application",
            "need access to",
        ]

        if any(keyword in text for keyword in access_keywords):

            return {
                "intent": "Service Request",
                "category": "Account and Access",
                "subcategory": "Application Access",
                "priority": "P2",
                "impact": "Individual",
                "urgency": "High",
                "assignment_group": "Identity and Access Management",
                "summary": "Corporate application access request",
                "automation_candidate": False,
                "confidence": 0.92,
            }

        # ---------------------------------------------------------
        # 3. VPN INCIDENT
        # ---------------------------------------------------------
        vpn_keywords = [
            "vpn",
            "virtual private network",
            "vpn authentication",
        ]

        if any(keyword in text for keyword in vpn_keywords):

            return {
                "intent": "Incident",
                "category": "Network",
                "subcategory": "VPN",
                "priority": "P2",
                "impact": "Individual",
                "urgency": "High",
                "assignment_group": "Network Support",
                "summary": "VPN authentication or connectivity failure",
                "automation_candidate": False,
                "confidence": 0.94,
            }

        # ---------------------------------------------------------
        # 4. WI-FI INCIDENT
        # ---------------------------------------------------------
        wifi_keywords = [
            "wifi",
            "wi-fi",
            "wireless",
        ]

        if any(keyword in text for keyword in wifi_keywords):

            return {
                "intent": "Incident",
                "category": "Network",
                "subcategory": "Wi-Fi",
                "priority": "P3",
                "impact": "Individual",
                "urgency": "Medium",
                "assignment_group": "Network Support",
                "summary": "Corporate Wi-Fi connectivity problem",
                "automation_candidate": True,
                "confidence": 0.91,
            }

        # ---------------------------------------------------------
        # 5. OUTLOOK INCIDENT
        # ---------------------------------------------------------
        outlook_keywords = [
            "outlook",
            "email synchronization",
            "email sync",
            "emails not syncing",
        ]

        if any(keyword in text for keyword in outlook_keywords):

            return {
                "intent": "Incident",
                "category": "Collaboration",
                "subcategory": "Outlook",
                "priority": "P3",
                "impact": "Individual",
                "urgency": "Medium",
                "assignment_group": "Collaboration Support",
                "summary": "Outlook email synchronization or connectivity issue",
                "automation_candidate": True,
                "confidence": 0.90,
            }

        # ---------------------------------------------------------
        # 6. LAPTOP PERFORMANCE INCIDENT
        # ---------------------------------------------------------
        performance_keywords = [
            "laptop is slow",
            "laptop slow",
            "laptop extremely slow",
            "my laptop is extremely slow",
            "computer is slow",
            "computer slow",
            "system is slow",
            "system slow",
            "poor performance",
            "performance issue",
            "computer is extremely slow",
        ]

        if any(keyword in text for keyword in performance_keywords):

            return {
                "intent": "Incident",
                "category": "Hardware and Performance",
                "subcategory": "Laptop Performance",
                "priority": "P3",
                "impact": "Individual",
                "urgency": "Medium",
                "assignment_group": "End User Computing",
                "summary": "Slow laptop or poor system performance",
                "automation_candidate": True,
                "confidence": 0.89,
            }

        # ---------------------------------------------------------
        # 7. SOFTWARE / PROVISIONING REQUEST
        # ---------------------------------------------------------
        software_keywords = [
            "install",
            "installation",
            "software",
            "visual studio code",
            "vs code",
            "postman",
            "chrome",
            "python",
            "7-zip",
        ]

        if any(keyword in text for keyword in software_keywords):

            return {
                "intent": "Service Request",
                "category": "Software and Applications",
                "subcategory": "Software Installation",
                "priority": "P3",
                "impact": "Individual",
                "urgency": "Medium",
                "assignment_group": "Endpoint Management",
                "summary": "Approved software installation request",
                "automation_candidate": True,
                "confidence": 0.94,
            }

        # ---------------------------------------------------------
        # 8. DEFAULT
        # ---------------------------------------------------------
        return {
            "intent": "Knowledge Question",
            "category": "General IT",
            "subcategory": "General Support",
            "priority": "P3",
            "impact": "Individual",
            "urgency": "Medium",
            "assignment_group": "IT Helpdesk",
            "summary": message[:100],
            "automation_candidate": False,
            "confidence": 0.60,
        }
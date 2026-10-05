from app.servicenow.client import ServiceNowClient


client = ServiceNowClient()


ticket = {
    "summary": "VPN authentication failure",
    "description": "User cannot connect to corporate VPN.",
    "category": "Network",
    "subcategory": "VPN",
    "priority": "P2",
    "assignment_group": "Network Support",
}


result = client.create_incident(ticket)


print("\nServiceNow Mock Test")
print("--------------------")
print(f"Incident Number: {result['number']}")
print(f"State: {result['state']}")
print(f"Message: {result['message']}")
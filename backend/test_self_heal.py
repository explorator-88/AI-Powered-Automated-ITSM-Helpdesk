from app.automation.agent import SelfHealAgent


agent = SelfHealAgent()

result = agent.handle(
    "My password has expired.",
    ticket_id="INC1002"
)

print("\nSELF-HEAL TEST")
print("--------------")
print(f"Status: {result['status']}")
print(f"Message: {result['message']}")
print(f"Automation: {result['automation']}")
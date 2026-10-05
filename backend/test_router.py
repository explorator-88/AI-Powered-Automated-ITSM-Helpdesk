from app.ai.router import AIRequestRouter


router = AIRequestRouter()


test_messages = [
    "My VPN authentication keeps failing",
    "My password has expired",
    "How do I fix Outlook synchronization?",
    "I need Visual Studio Code installed",
    "My laptop is extremely slow",
    "I need access to the HR application",
]


for message in test_messages:

    result = router.classify(message)

    print("\n" + "=" * 60)
    print(f"USER: {message}")
    print(f"INTENT: {result['intent']}")
    print(f"CATEGORY: {result['category']}")
    print(f"SUBCATEGORY: {result['subcategory']}")
    print(f"PRIORITY: {result['priority']}")
    print(f"ASSIGNMENT: {result['assignment_group']}")
    print(f"CONFIDENCE: {result['confidence']}")
    print(f"AUTOMATION: {result['automation_candidate']}")
from app.automation.actions import execute_action


print("\nTesting approved automation")
print("---------------------------")

result = execute_action(
    "password_reset",
    username="employee"
)

print(result)


print("\nTesting blocked automation")
print("--------------------------")

blocked = execute_action(
    "delete_database"
)

print(blocked)
from datetime import datetime, timezone

APPROVED_SOFTWARE = {
    "Visual Studio Code",
    "Google Chrome",
    "Python",
    "Postman",
    "7-Zip",
    "Git",
}


def provision_software(software_name: str, username: str = "employee") -> dict:
    if software_name not in APPROVED_SOFTWARE:
        return {
            "status": "blocked",
            "software": software_name,
            "message": "Software is not approved for automated provisioning.",
        }

    return {
        "status": "completed",
        "software": software_name,
        "username": username,
        "message": f"{software_name} provisioning completed successfully.",
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
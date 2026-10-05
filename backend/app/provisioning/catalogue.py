SOFTWARE_CATALOGUE = {
    "Visual Studio Code": {
        "software_id": "SW001",
        "name": "Visual Studio Code",
        "category": "Development Tools",
        "approved": True,
    },
    "Google Chrome": {
        "software_id": "SW002",
        "name": "Google Chrome",
        "category": "Browser",
        "approved": True,
    },
    "Python": {
        "software_id": "SW003",
        "name": "Python",
        "category": "Development Tools",
        "approved": True,
    },
    "Postman": {
        "software_id": "SW004",
        "name": "Postman",
        "category": "Development Tools",
        "approved": True,
    },
    "7-Zip": {
        "software_id": "SW005",
        "name": "7-Zip",
        "category": "Utilities",
        "approved": True,
    },
    "Git": {
        "software_id": "SW006",
        "name": "Git",
        "category": "Development Tools",
        "approved": True,
    },
}


def find_software(query: str) -> dict | None:
    query = query.lower().strip()

    aliases = {
        "vs code": "Visual Studio Code",
        "visual studio code": "Visual Studio Code",
        "chrome": "Google Chrome",
        "google chrome": "Google Chrome",
        "python": "Python",
        "postman": "Postman",
        "7zip": "7-Zip",
        "7-zip": "7-Zip",
        "git": "Git",
    }

    for alias, software_name in aliases.items():
        if alias in query:
            return SOFTWARE_CATALOGUE[software_name]

    for software_name, details in SOFTWARE_CATALOGUE.items():
        if software_name.lower() in query:
            return details

    return None
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ai_itsm")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not configured")

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

tickets_collection = db["tickets"]
knowledge_collection = db["knowledge"]
chat_collection = db["chat_sessions"]
automation_collection = db["automation_actions"]
software_collection = db["software_requests"]
audit_collection = db["audit_logs"]
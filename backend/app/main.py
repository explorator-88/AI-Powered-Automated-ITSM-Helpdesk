from app.api.chatbot import router as chatbot_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.test_db import router as test_db_router


app = FastAPI(
    title="AI ITSM Helpdesk API",
    version="1.0.0",
)

app.include_router(
    chatbot_router,
    prefix="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    test_db_router,
    prefix="/api",
)


@app.get("/")
def root():
    return {
        "message": "AI ITSM Helpdesk API",
        "status": "running",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
    }
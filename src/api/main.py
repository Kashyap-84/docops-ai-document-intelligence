from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="DocOps AI - Document Intelligence API",
    description="OCR-based document extraction MVP with schema validation and human review routing.",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def root() -> dict:
    return {
        "message": "DocOps AI API is running",
        "docs": "/docs",
        "health": "/api/v1/health",
    }

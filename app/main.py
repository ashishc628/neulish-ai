from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="Neulish AI Engine",
    version="1.0",
    description="Regulation-first AI for cognitive wellness"
)

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Neulish AI Engine",
        "message": "Go to /docs for API documentation"
    }

app.include_router(router)

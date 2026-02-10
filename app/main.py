from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="Neulish AI Engine",
    description="Gentle, regulation-first cognitive wellness recommendations",
    version="v1"
)

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Neulish AI Engine",
        "message": "Go to /docs for API documentation"
    }

app.include_router(router)

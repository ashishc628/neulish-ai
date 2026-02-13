from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="Neulish AI Engine",
    version="2.0",
    description="Regulation-first cognitive wellness AI"
)

# Include API routes
app.include_router(router)

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Neulish AI Engine",
        "message": "Go to /docs for API documentation"
    }

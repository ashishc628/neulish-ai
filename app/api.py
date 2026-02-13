from fastapi import APIRouter
from app.schemas import UserPayload
from ml.model import analyze_user

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "engine": "Neulish AI v2"}

@router.post("/analyze-user")
def analyze(payload: UserPayload):
    return analyze_user(payload.dict())

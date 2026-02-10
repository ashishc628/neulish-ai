from fastapi import APIRouter
from app.schemas import UserInput
from ml.model import recommend

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "neulish-ai",
        "version": "v1"
    }

@router.post("/recommend")
def get_recommendation(data: UserInput):
    return recommend(data.dict())


@router.post("/weekly-summary")
def weekly_summary(data: list):
    from app.weekly_summary import generate_weekly_summary
    return generate_weekly_summary(data)

@router.post("/corporate/analytics")
def corporate_analytics(data: list):
    from app.corporate_analytics import generate_corporate_metrics
    return generate_corporate_metrics(data)

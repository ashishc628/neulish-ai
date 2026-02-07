from fastapi import APIRouter
from app.schemas import UserInput
from ml.model import recommend

router = APIRouter()

@router.post("/recommend")
def get_recommendation(data: UserInput):
    return recommend(data.dict())

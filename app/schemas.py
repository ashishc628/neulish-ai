from pydantic import BaseModel
from typing import Optional, Literal

class UserInput(BaseModel):
    stress_level: Optional[int] = 5          # 0–10 slider
    energy_level: Optional[int] = 5          # 0–10 slider
    recent_focus_level: Optional[int] = 5    # 0–10 slider
    sleep_quality: Optional[int] = 5         # 0–10 slider
    sleep_duration_hours: Optional[float] = 7.0
    time_of_day: Literal["morning", "afternoon", "evening", "night"] = "afternoon"

from pydantic import BaseModel
from typing import Literal, Optional

class UserInput(BaseModel):
    # Sleep (raw values from UI / device)
    sleep_duration_hours: Optional[float] = 7.0
    sleep_quality: Optional[int] = 5          # 0–10 slider

    # Mental state (0–10 sliders)
    stress_level: Optional[int] = 5            # 0–10
    energy_level: Optional[int] = 5            # 0–10
    recent_focus_level: Optional[int] = 5      # 0–10

    # Context
    time_of_day: Literal["morning", "afternoon", "evening", "night"] = "afternoon"

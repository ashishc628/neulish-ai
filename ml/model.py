from ml.utils import clamp, normalize_10_to_5

def recommend(user: dict):
    sleep = clamp(user.get("sleep_duration_hours", 7.0), 0, 12)
    sleep_q = normalize_10_to_5(user.get("sleep_quality", 5))
    stress  = normalize_10_to_5(user.get("stress_level", 5))
    energy  = normalize_10_to_5(user.get("energy_level", 5))
    focus   = normalize_10_to_5(user.get("recent_focus_level", 5))
    time_of_day = user.get("time_of_day", "afternoon")

    recommendations = []

    # 🚨 SAFETY FIRST
    if time_of_day == "night" or sleep < 6 or sleep_q <= 2:
        return {
            "confidence_label": "Gentle",
            "recommendations": [
                {
                    "type": "meditation",
                    "name": "Sleep Wind-Down",
                    "duration": 10,
                    "description": "Rest and nervous system recovery come first."
                }
            ],
            "explanation": "Sleep and timing indicate rest is the priority."
        }

    # 🧘 Regulation First
    recommendations.append({
        "type": "meditation",
        "name": "Body Scan & Breathe",
        "duration": 3 if stress <= 3 else 7,
        "description": "Grounding breath to prepare your nervous system."
    })

    # 🧩 Memory Pattern
    if energy >= 3:
        recommendations.append({
            "type": "game",
            "name": "Memory Pattern",
            "duration": 5,
            "description": "Gentle spatial recall for working memory."
        })

    # 🔢 Number Flow
    if energy >= 4 and focus >= 4 and stress <= 2:
        recommendations.append({
            "type": "game",
            "name": "Number Flow",
            "duration": 5,
            "description": "Calm sequencing for executive focus."
        })

    # 😴 Optional Wind-Down
    if sleep >= 7 and sleep_q >= 4 and energy >= 4:
        recommendations.append({
            "type": "meditation",
            "name": "Sleep Wind-Down",
            "duration": 10,
            "description": "Optional reminder to close the day calmly."
        })

    label = "Active" if energy >= 4 and stress <= 2 else "Balanced"

    return {
        "confidence_label": label,
        "recommendations": recommendations,
        "explanation": "Plan adapted using sleep, stress, energy, focus, and time of day."
    }

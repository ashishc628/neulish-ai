# -----------------------------
# Utility helpers (ALWAYS FIRST)
# -----------------------------

def clamp(value, min_value, max_value):
    try:
        value = float(value)
        return max(min_value, min(value, max_value))
    except:
        return min_value


def normalize_10_to_5(value):
    """
    Converts 0–10 scale to 1–5 scale safely
    """
    try:
        value = float(value)
        value = max(0, min(value, 10))
        return int(round((value / 10) * 4 + 1))
    except:
        return 3

def recommend(user: dict):

    sleep = clamp(user.get("sleep_duration_hours", 7.0), 0, 12)

    sleep_q = normalize_10_to_5(user.get("sleep_quality", 5))
    stress = normalize_10_to_5(user.get("stress_level", 5))
    energy = normalize_10_to_5(user.get("energy_level", 5))
    focus = normalize_10_to_5(user.get("recent_focus_level", 5))

    time_of_day = user.get("time_of_day", "afternoon")

    recommendations = []

    sleep = user["sleep_duration_hours"]
    sleep_q = user["sleep_quality"]
    stress = user["stress_level"]
    energy = user["energy_level"]
    time_of_day = user["time_of_day"]
    focus = user["recent_focus_level"]

    # -----------------------
    # 1. NIGHT OR POOR SLEEP
    # -----------------------
    if time_of_day == "night" or sleep < 6 or sleep_q <= 2:
        return {
            "recommendations": [
                {
                    "type": "meditation",
                    "name": "Sleep Wind-Down",
                    "duration": 10,
                    "description": "A passive session to help the brain settle before rest."
                }
            ],
            "explanation": "Sleep and timing suggest rest is the priority."
        }

    # -----------------------
    # 2. ALWAYS START WITH REGULATION
    # -----------------------
    recommendations.append({
        "type": "meditation",
        "name": "Body Scan & Breathe",
        "duration": 3 if stress <= 3 else 7,
        "description": "Grounding breath to prepare the nervous system."
    })

    # -----------------------
    # 3. MEMORY PATTERN (SAFE DEFAULT GAME)
    # -----------------------
    if energy >= 3:
        recommendations.append({
            "type": "game",
            "name": "Memory Pattern",
            "duration": 5,
            "description": "Gentle spatial recall to support working memory."
        })

    # -----------------------
    # 4. NUMBER FLOW (ONLY IF HIGH FOCUS)
    # -----------------------
    if energy >= 4 and focus >= 4 and stress <= 2:
        recommendations.append({
            "type": "game",
            "name": "Number Flow",
            "duration": 5,
            "description": "Calm sequencing exercise for executive attention."
        })

    # -----------------------
    # 5. OPTIONAL SLEEP SUPPORT ON GOOD DAYS
    # -----------------------
    if sleep >= 7 and sleep_q >= 4 and energy >= 4 and stress <= 2:
        recommendations.append({
            "type": "meditation",
            "name": "Sleep Wind-Down",
            "duration": 10,
            "description": "Optional reminder to end the day calmly."
        })

    return {
        "recommendations": recommendations,
        "explanation": "Plan adapted using sleep, stress, energy, focus, and time of day."
    }

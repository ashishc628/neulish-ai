import numpy as np
from statistics import mean


def extract_features(user):
    checkins = user.get("dailyCheckIns", [])
    memory_sessions = user.get("activities", {}).get("memoryGrid", {}).get("sessions", [])
    number_sessions = user.get("activities", {}).get("numberFlow", {}).get("sessions", [])
    breathe_sessions = user.get("activities", {}).get("relaxBreathe", {}).get("sessions", [])
    sleep_sessions = user.get("activities", {}).get("sleepWindow", {}).get("sessions", [])

    # ---- DAILY AVERAGES ----
    stress = [c["energy"]["stressed"] for c in checkins]
    focus = [c["energy"]["focused"] for c in checkins]
    calm = [c["energy"]["calm"] for c in checkins]
    tired = [c["energy"]["tired"] for c in checkins]
    sleep_q = [c["sleepQuality"]["sleep_quality"] for c in checkins]
    sleep_h = [c["sleepQuality"]["sleep_duration_hours"] for c in checkins]

    features = {
        "avg_stress": mean(stress) if stress else 0,
        "avg_focus": mean(focus) if focus else 0,
        "avg_calm": mean(calm) if calm else 0,
        "avg_tired": mean(tired) if tired else 0,
        "avg_sleep_quality": mean(sleep_q) if sleep_q else 0,
        "avg_sleep_hours": mean(sleep_h) if sleep_h else 0,
        "memory_errors": mean([s["data"]["incorrectAttempts"] for s in memory_sessions]) if memory_sessions else 0,
        "number_score": mean([s["data"]["score"] for s in number_sessions]) if number_sessions else 0,
        "meditation_count": len(breathe_sessions),
        "sleep_count": len(sleep_sessions)
    }

    return features


def generate_recommendation(features):

    activities = []
    explanation = []

    # High stress → meditation
    if features["avg_stress"] > 6:
        activities.append({"activityType": "relax_breathe", "durationMinutes": 5})
        explanation.append("Stress elevated → regulation first.")

    # Poor sleep → sleep window
    if features["avg_sleep_hours"] < 6.5:
        activities.append({"activityType": "sleep_window", "durationMinutes": 10})
        explanation.append("Sleep duration low → wind-down recommended.")

    # Low focus → memory + number
    if features["avg_focus"] < 5:
        activities.append({"activityType": "memory_grid", "durationMinutes": 5})
        activities.append({"activityType": "number_flow", "durationMinutes": 3})
        explanation.append("Focus slightly reduced → gentle cognitive stimulation.")

    # High functioning day
    if features["avg_focus"] > 7 and features["avg_stress"] < 4:
        activities.append({"activityType": "memory_grid", "durationMinutes": 7})
        activities.append({"activityType": "number_flow", "durationMinutes": 5})
        explanation.append("Stable day → progressive challenge.")

    confidence = "gentle"
    if features["avg_focus"] > 6 and features["avg_stress"] < 5:
        confidence = "moderate"

    return activities, explanation, confidence


def generate_weekly_summary(features):
    return {
        "stress_trend": "moderate" if features["avg_stress"] > 5 else "stable",
        "focus_level": round(features["avg_focus"], 2),
        "sleep_average": round(features["avg_sleep_hours"], 2),
        "recommendation_strategy": "regulation-first"
    }


def analyze_user(payload):

    results = []

    for user in payload["users"]:
        features = extract_features(user)
        activities, explanation, confidence = generate_recommendation(features)
        weekly_summary = generate_weekly_summary(features)

        results.append({
            "uid": user["uid"],
            "todayRecommendation": activities,
            "confidence_label": confidence,
            "explanation": explanation,
            "weeklySummary": weekly_summary
        })

    return {"results": results}

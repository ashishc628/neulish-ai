from datetime import datetime, timedelta
import numpy as np

def generate_weekly_summary(week_data: list):
    if not week_data:
        return {"summary": ["No data this week."], "confidence_label": "Neutral"}

    sleep_hours = [d["sleep_duration"] for d in week_data if d.get("sleep_duration")]
    stress = [d["stress"] for d in week_data if d.get("stress")]

    summary = []

    if sleep_hours:
        avg_sleep = round(np.mean(sleep_hours), 1)
        summary.append(f"You averaged about {avg_sleep} hours of sleep.")

        if np.std(sleep_hours) < 1:
            summary.append("Your sleep schedule was fairly consistent.")

    if stress and np.mean(stress) < 4:
        summary.append("Stress levels were generally manageable this week.")
    elif stress:
        summary.append("Some days felt more demanding than others.")

    summary.append(
        "Consistency mattered more than session length this week."
    )

    return {
        "week": "last 7 days",
        "tone": "gentle",
        "summary": summary,
        "suggestion": "Next week, keep sessions short on busy days.",
        "confidence_label": "Steady"
    }

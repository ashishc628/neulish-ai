def generate_corporate_metrics(users_week_data: list):
    total_users = len(users_week_data)
    if total_users == 0:
        return {}

    sessions = []
    stress = []
    breathing_first = 0

    for user in users_week_data:
        sessions.append(user["sessions"])
        stress.append(user["avg_stress"])
        if user["started_with_breathing"]:
            breathing_first += 1

    return {
        "active_users": total_users,
        "avg_sessions_per_user": round(sum(sessions) / total_users, 2),
        "avg_stress_level": round(sum(stress) / total_users, 2),
        "breathing_first_sessions_pct": round(breathing_first / total_users, 2)
    }

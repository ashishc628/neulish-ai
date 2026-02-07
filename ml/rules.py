def apply_safety_rules(user, duration):
    if user["sleep_duration_hours"] < 6:
        return min(duration, 5)

    if user["stress_level"] >= 4:
        return min(duration, 4)

    return max(duration, 2)

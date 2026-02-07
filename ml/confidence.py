def get_confidence_label(user):
    sleep = user["sleep_duration_hours"]
    sleep_q = user["sleep_quality"]
    stress = user["stress_level"]
    energy = user["energy_level"]

    if sleep < 6 or sleep_q <= 2 or stress >= 4:
        return {
            "label": "Gentle Day",
            "description": "A calm, low-pressure day focused on regulation and rest."
        }

    if energy >= 4 and stress <= 2 and sleep >= 7:
        return {
            "label": "Active Day",
            "description": "You seem ready for focused cognitive activity today."
        }

    return {
        "label": "Moderate Day",
        "description": "A balanced day for light focus and gentle regulation."
    }

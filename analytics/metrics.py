def aggregate(df):
    return {
        "avg_sleep": df["sleep_duration_hours"].mean(),
        "avg_stress": df["stress_level"].mean(),
        "completion_rate": df["completed_session"].mean()
    }

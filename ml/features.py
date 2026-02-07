import pandas as pd

REQUIRED_FEATURES = {
    "energy_level": 3,
    "stress_level": 3,
    "mood_score": 3,
    "sleep_duration_hours": 7,
    "sleep_quality": 3,
    "journal_sentiment": 0,
    "emotional_intensity": 2,
    "numbers_tap_accuracy": 0.7,
    "memory_grid_accuracy": 0.7
}


def preprocess(df: pd.DataFrame):
    df = df.copy()

    # Map categorical values safely
    if "journal_sentiment" in df.columns:
        df["journal_sentiment"] = df["journal_sentiment"].map(
            {"negative": -1, "neutral": 0, "positive": 1}
        )

    if "emotional_intensity" in df.columns:
        df["emotional_intensity"] = df["emotional_intensity"].map(
            {"low": 1, "medium": 2, "high": 3}
        )

    # Ensure all required features exist
    for feature, default in REQUIRED_FEATURES.items():
        if feature not in df.columns:
            df[feature] = default

    df.fillna(0, inplace=True)

    return df[list(REQUIRED_FEATURES.keys())]

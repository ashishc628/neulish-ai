import joblib
import pandas as pd

def update_model(new_data: pd.DataFrame):
    model = joblib.load("models/duration_model.pkl")

    X = new_data.drop(columns=["recommended_duration_minutes"])
    y = new_data["recommended_duration_minutes"]

    model.fit(X, y)
    joblib.dump(model, "models/duration_model.pkl")

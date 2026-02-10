import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("ml/data/neulish_training_data.csv")

X = df[["stress", "focus"]]
y = df["rec_memory"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

joblib.dump(model, "ml/models/recommendation_models.pkl")
print("✅ Model trained and saved")

import pandas as pd
import joblib
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from ml.features import preprocess

# Load data
df = pd.read_csv("data/input_data.csv")

# -----------------------------
# FEATURES
# -----------------------------
X = preprocess(df)

# -----------------------------
# CLUSTERING (user state patterns)
# -----------------------------
cluster_model = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)
df["state_cluster"] = cluster_model.fit_predict(X)

# -----------------------------
# TARGET (IMPORTANT FIX)
# -----------------------------
TARGET_COLUMN = "ai_session_length_min"

if TARGET_COLUMN not in df.columns:
    raise ValueError(
        f"Target column '{TARGET_COLUMN}' not found in CSV."
    )

y = df[TARGET_COLUMN]

# -----------------------------
# DURATION PREDICTION MODEL
# -----------------------------
duration_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=8,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

duration_model.fit(X, y)

# -----------------------------
# SAVE MODELS
# -----------------------------
joblib.dump(cluster_model, "models/cluster.pkl")
joblib.dump(duration_model, "models/duration_model.pkl")

print("✅ Models trained successfully.")
print(f"   Samples trained: {len(df)}")
print(f"   Target used: {TARGET_COLUMN}")

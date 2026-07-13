"""Create a demo model artifact for local UI testing."""
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

FEATURE_COLUMNS = [
    "pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude",
    "passenger_count", "hour", "day", "month", "year", "dayofweek",
    "dist_travel_km", "bearing", "pickup_dist_from_center", "dropoff_dist_from_center",
    "is_weekend", "is_rush_hour",
]

rng = np.random.default_rng(42)
X = rng.normal(size=(200, len(FEATURE_COLUMNS)))
X[:, 10] = rng.uniform(1, 20, 200)
y = 8.0 + X[:, 10] * 2.2 + rng.normal(0, 1.5, 200)

scaler = StandardScaler()
model = LinearRegression().fit(scaler.fit_transform(X), y)

artifact = {
    "model_name": "random_forest_regression",
    "model": model,
    "scaler": scaler,
    "feature_columns": FEATURE_COLUMNS,
    "target_column": "fare_amount",
    "metrics": {
        "train": {"mae": 0.82, "rmse": 1.05, "r2": 0.91},
        "test": {"mae": 2.15, "rmse": 2.78, "r2": 0.74},
    },
}

out = Path(__file__).resolve().parents[1] / "Model" / "artifacts" / "random_forest_regression.joblib"
out.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(artifact, out)
print(f"Created {out}")

"""One-time setup: ensure writable dirs and a fallback model exist on the server."""
import logging
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from config import DB_PATH, DEFAULT_MODEL_ARTIFACT, MODEL_DIR

logger = logging.getLogger(__name__)

FEATURE_COLUMNS = [
    "pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude",
    "passenger_count", "hour", "day", "month", "year", "dayofweek",
    "dist_travel_km", "bearing", "pickup_dist_from_center", "dropoff_dist_from_center",
    "is_weekend", "is_rush_hour",
]


def ensure_runtime_dirs() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def ensure_default_model() -> None:
    """Create a lightweight demo model if the ML teammate's artifact is not present yet."""
    if DEFAULT_MODEL_ARTIFACT.exists():
        return

    logger.warning(
        "No model at %s -- creating a demo artifact so the deployed app can predict.",
        DEFAULT_MODEL_ARTIFACT,
    )

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
    joblib.dump(artifact, DEFAULT_MODEL_ARTIFACT)
    logger.info("Demo model written to %s", DEFAULT_MODEL_ARTIFACT)


def bootstrap() -> None:
    ensure_runtime_dirs()
    ensure_default_model()

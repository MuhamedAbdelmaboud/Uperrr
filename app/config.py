"""Central configuration for the Uber Fare Prediction app.

Single source of truth for paths, constants, and app-wide settings.
Nothing in ui/, core/, or db/ should hardcode a path or magic number
that belongs here — import from config instead (Open/Closed friendly:
change a value once, it propagates everywhere).
"""
from dataclasses import dataclass, field
from pathlib import Path

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parents[1]          # uber-fare-app/
MODEL_DIR = BASE_DIR / "Model" / "artifacts"
DB_PATH = BASE_DIR / "app" / "db" / "predictions.db"

# Which trained model artifact the app loads by default.
# Must match one of the *.joblib filenames produced by Model/training.py
DEFAULT_MODEL_ARTIFACT = MODEL_DIR / "random_forest_regression.joblib"

# All artifacts available for the "Model Comparison" tab.
# (name shown in UI) -> (joblib filename)
AVAILABLE_MODEL_ARTIFACTS: dict[str, str] = {
    "Random Forest": "random_forest_regression.joblib",
    "Gradient Boosting": "gradient_boosting_regression.joblib",
    "Decision Tree": "decision_tree_regression.joblib",
    "Linear Regression": "linear_regression.joblib",
    "Ridge Regression": "ridge_regression.joblib",
    "Lasso Regression": "lasso_regression.joblib",
}


# ──────────────────────────────────────────────
# Geography (must match Preprocessing/featuring.py)
# ──────────────────────────────────────────────

@dataclass(frozen=True)
class CityCenter:
    name: str
    lat: float
    lon: float


NYC_CENTER = CityCenter(name="Times Square, NYC", lat=40.7580, lon=-73.9855)

# Default map view when the app first loads (centered on NYC).
MAP_DEFAULT_ZOOM = 12
MAP_DEFAULT_LAT = NYC_CENTER.lat
MAP_DEFAULT_LON = NYC_CENTER.lon

# Sanity bounds — reject clicks way outside the metro area the model
# was trained on (mirrors RangeFilter bounds in preprocessing, but
# tighter, since the model has no real signal far outside NYC).
COORDINATE_BOUNDS = {
    "lat_min": 40.4,
    "lat_max": 41.1,
    "lon_min": -74.5,
    "lon_max": -73.3,
}


# ──────────────────────────────────────────────
# Trip / fare business rules
# ──────────────────────────────────────────────

RUSH_HOUR_WINDOWS = ((7, 9), (16, 19))   # (start_hour, end_hour), inclusive
WEEKEND_DAYS = (6, 7)                     # dayofweek: 1=Mon ... matches teammate's +1 convention

MAX_PASSENGERS = 4
MIN_PASSENGERS = 1


@dataclass(frozen=True)
class RideType:
    key: str
    label: str
    multiplier: float
    capacity: int


RIDE_TYPES: tuple[RideType, ...] = (
    RideType(key="economy", label="UberX", multiplier=1.0, capacity=4),
    RideType(key="comfort", label="Comfort", multiplier=1.25, capacity=4),
    RideType(key="xl", label="UberXL", multiplier=1.55, capacity=6),
)

# Rough "surge" nudge for the UI's confidence/estimate display.
# NOT part of the trained model — purely a presentation-layer multiplier
# applied on top of the predicted fare when is_rush_hour == 1.
RUSH_HOUR_SURGE_MULTIPLIER = 1.15

# Average city driving speed used ONLY to estimate trip duration for the UI
# (not part of the trained model — the model never sees a time feature like this).
AVG_SPEED_KMH = 24.0          # normal NYC traffic
AVG_SPEED_KMH_RUSH_HOUR = 14.0


# ──────────────────────────────────────────────
# App metadata / theme tokens
# ──────────────────────────────────────────────

APP_TITLE = "FareCast"
APP_TAGLINE = "Know your fare before you go."

# NOTE on fonts: Uber's real product typeface is "Uber Move", a proprietary
# font not licensed for public/web embedding. "Inter" is the closest widely
# available open-source match — same grotesk-sans structure, similar
# weight range, and it's what most Uber-style clones use for this reason.
FONT_FAMILY = "'Inter', -apple-system, 'Helvetica Neue', Arial, sans-serif"
GOOGLE_FONT_URL = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"


@dataclass(frozen=True)
class Theme:
    bg: str = "#FFFFFF"
    surface: str = "#F6F6F6"
    surface_alt: str = "#EDEDED"
    text_primary: str = "#000000"
    text_secondary: str = "#545454"
    accent: str = "#000000"      # Uber's CTAs are solid black, not a color accent
    accent_soft: str = "#F6F6F6"
    warning: str = "#C0362C"
    border: str = "#E2E2E2"


THEME = Theme()


# ──────────────────────────────────────────────
# Misc
# ──────────────────────────────────────────────

LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
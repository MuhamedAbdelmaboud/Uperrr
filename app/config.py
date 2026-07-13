"""Central configuration for the Uber Fare Prediction app."""
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "Model" / "artifacts"
DB_PATH = BASE_DIR / "app" / "db" / "predictions.db"

DEFAULT_MODEL_ARTIFACT = MODEL_DIR / "random_forest_regression.joblib"

AVAILABLE_MODEL_ARTIFACTS: dict[str, str] = {
    "Random Forest": "random_forest_regression.joblib",
    "Gradient Boosting": "gradient_boosting_regression.joblib",
    "Decision Tree": "decision_tree_regression.joblib",
    "Linear Regression": "linear_regression.joblib",
    "Ridge Regression": "ridge_regression.joblib",
    "Lasso Regression": "lasso_regression.joblib",
}


@dataclass(frozen=True)
class CityCenter:
    name: str
    lat: float
    lon: float


NYC_CENTER = CityCenter(name="New York City", lat=40.7580, lon=-73.9855)

MAP_DEFAULT_ZOOM = 12
MAP_DEFAULT_LAT = NYC_CENTER.lat
MAP_DEFAULT_LON = NYC_CENTER.lon

COORDINATE_BOUNDS = {
    "lat_min": 40.4,
    "lat_max": 41.1,
    "lon_min": -74.5,
    "lon_max": -73.3,
}

RUSH_HOUR_WINDOWS = ((7, 9), (16, 19))
WEEKEND_DAYS = (6, 7)

MAX_PASSENGERS = 4
MIN_PASSENGERS = 1


@dataclass(frozen=True)
class RideType:
    key: str
    label: str
    description: str
    multiplier: float
    capacity: int


RIDE_TYPES: tuple[RideType, ...] = (
    RideType(key="economy", label="UberX", description="Affordable rides", multiplier=1.0, capacity=4),
    RideType(key="comfort", label="Comfort", description="Newer cars, extra legroom", multiplier=1.25, capacity=4),
    RideType(key="xl", label="UberXL", description="Fits up to 6 passengers", multiplier=1.55, capacity=6),
)

RUSH_HOUR_SURGE_MULTIPLIER = 1.15
AVG_SPEED_KMH = 24.0
AVG_SPEED_KMH_RUSH_HOUR = 14.0

APP_TITLE = "FareCast"
APP_TAGLINE = "Plan your trip. Know your fare."
APP_CITY = "New York City"

FONT_FAMILY = "'Inter', -apple-system, 'Helvetica Neue', Arial, sans-serif"
GOOGLE_FONT_URL = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"


@dataclass(frozen=True)
class Theme:
    bg: str = "#FFFFFF"
    surface: str = "#F6F6F6"
    surface_alt: str = "#EDEDED"
    surface_hover: str = "#E8E8E8"
    text_primary: str = "#000000"
    text_secondary: str = "#545454"
    text_muted: str = "#8A8A8A"
    accent: str = "#000000"
    success: str = "#06C167"
    warning: str = "#C0362C"
    border: str = "#E2E2E2"
    pickup: str = "#000000"
    dropoff: str = "#545454"
    map_route: str = "#000000"


THEME = Theme()
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

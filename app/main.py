import logging
import sys
from pathlib import Path
 
import streamlit as st
 
# Allow `import config`, `import core.x`, etc. when run as `streamlit run app/main.py`
sys.path.insert(0, str(Path(__file__).resolve().parent))
 
from config import (  # noqa: E402
    APP_TAGLINE, APP_TITLE, DB_PATH, DEFAULT_MODEL_ARTIFACT, FONT_FAMILY,
    GOOGLE_FONT_URL, LOG_FORMAT, THEME,
)
from core.eta import estimate_minutes  # noqa: E402
from core.feature_builder import TripFeatureBuilder, TripRequest  # noqa: E402
from core.predictor import JoblibPredictor, ModelArtifactNotFoundError  # noqa: E402
from core.pricing import quote_price  # noqa: E402
from db.models import PredictionRecord  # noqa: E402
from db.repository import SQLitePredictionRepository  # noqa: E402
from ui.history import render_history  # noqa: E402
from ui.map_view import render_map  # noqa: E402
from ui.model_comparison import render_model_comparison  # noqa: E402
from ui.results import render_results  # noqa: E402
from ui.sidebar import render_sidebar  # noqa: E402
 
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)
 
 
def inject_theme() -> None:
    st.markdown(f'<link href="{GOOGLE_FONT_URL}" rel="stylesheet">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: {FONT_FAMILY};
        }}
        .stApp {{
            background-color: {THEME.bg};
            color: {THEME.text_primary};
        }}
        h1, h2, h3 {{
            font-weight: 700;
            letter-spacing: -0.02em;
        }}
        div[data-testid="stMetric"] {{
            background-color: {THEME.surface};
            border: 1px solid {THEME.border};
            border-radius: 12px;
            padding: 1rem;
        }}
        div[data-testid="stMetricValue"] {{
            color: {THEME.text_primary};
        }}
        .stButton > button {{
            background-color: {THEME.accent};
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.6rem 1rem;
        }}
        .stButton > button:hover {{
            background-color: #222222;
            color: #FFFFFF;
        }}
        .stButton > button:disabled {{
            background-color: {THEME.surface_alt};
            color: {THEME.text_secondary};
        }}
        div[data-baseweb="radio"] label {{
            font-weight: 500;
        }}
        .trip-panel {{
            background-color: {THEME.surface};
            border: 1px solid {THEME.border};
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
 
 
@st.cache_resource
def get_repository() -> SQLitePredictionRepository:
    return SQLitePredictionRepository(DB_PATH)
 
 
@st.cache_resource
def get_predictor() -> JoblibPredictor | None:
    try:
        return JoblibPredictor(DEFAULT_MODEL_ARTIFACT)
    except ModelArtifactNotFoundError as exc:
        logger.warning("%s", exc)
        return None
 
 
def render_predict_tab(predictor, repository) -> None:
    if predictor is None:
        st.warning(
            "No trained model found yet — fare prediction will switch on "
            "automatically once the ML teammate's `Model/training.py` artifact "
            f"lands at `{DEFAULT_MODEL_ARTIFACT}`. Map and inputs still work below."
        )
 
    col_map, col_results = st.columns([2, 1])
 
    with col_map:
        st.markdown('<div class="trip-panel">', unsafe_allow_html=True)
        sidebar_values = render_sidebar()
        st.markdown("</div>", unsafe_allow_html=True)
        pickup, dropoff = render_map()
 
    with col_results:
        quote = None
        eta_minutes = None
 
        ready = pickup is not None and dropoff is not None
        get_estimate = st.button(
            "Get fare estimate", type="primary", use_container_width=True, disabled=not ready,
        )
 
        if get_estimate and ready and predictor is not None:
            trip = TripRequest(
                pickup_lat=pickup[0], pickup_lon=pickup[1],
                dropoff_lat=dropoff[0], dropoff_lon=dropoff[1],
                passenger_count=sidebar_values["passenger_count"],
                pickup_datetime=sidebar_values["pickup_datetime"],
            )
            features = TripFeatureBuilder().build(trip)
            prediction = predictor.predict(features)
 
            is_rush_hour = bool(features["is_rush_hour"].iloc[0])
            ride_type = sidebar_values["ride_type"]
            quote = quote_price(prediction, ride_type, is_rush_hour)
            eta_minutes = estimate_minutes(
                float(features["dist_travel_km"].iloc[0]), is_rush_hour,
            )
 
            repository.save(PredictionRecord(
                pickup_lat=trip.pickup_lat, pickup_lon=trip.pickup_lon,
                dropoff_lat=trip.dropoff_lat, dropoff_lon=trip.dropoff_lon,
                pickup_datetime=trip.pickup_datetime.isoformat(),
                passenger_count=trip.passenger_count, ride_type=ride_type.key,
                dist_travel_km=float(features["dist_travel_km"].iloc[0]),
                is_weekend=int(features["is_weekend"].iloc[0]),
                is_rush_hour=int(is_rush_hour),
                model_name=quote.model_name, predicted_fare=quote.final_fare,
            ))
        elif get_estimate and predictor is None:
            st.error("Can't predict yet — no trained model artifact available.")
 
        render_results(quote, eta_minutes)
 
 
def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    inject_theme()
 
    st.title(APP_TITLE)
    st.caption(APP_TAGLINE)
 
    repository = get_repository()
    predictor = get_predictor()
 
    tab_predict, tab_history, tab_models = st.tabs(
        ["Predict", "History", "Model Comparison"]
    )
 
    with tab_predict:
        render_predict_tab(predictor, repository)
    with tab_history:
        render_history(repository)
    with tab_models:
        render_model_comparison()
 
 
if __name__ == "__main__":
    main()
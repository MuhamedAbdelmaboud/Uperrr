"""Interactive map: click once for pickup, click again for dropoff.

Third click starts a new trip (pickup resets, dropoff clears). A straight
route-preview line is drawn between the two points once both are set —
this is a visual preview only, not a routed path (no routing API used).
"""
import folium
import streamlit as st
from streamlit_folium import st_folium

from config import COORDINATE_BOUNDS, MAP_DEFAULT_LAT, MAP_DEFAULT_LON, MAP_DEFAULT_ZOOM, THEME

PICKUP_KEY = "trip_pickup"
DROPOFF_KEY = "trip_dropoff"


def _in_bounds(lat: float, lon: float) -> bool:
    b = COORDINATE_BOUNDS
    return b["lat_min"] <= lat <= b["lat_max"] and b["lon_min"] <= lon <= b["lon_max"]


def _handle_click(lat: float, lon: float) -> None:
    if not _in_bounds(lat, lon):
        st.warning(
            "That point is outside the area the model was trained on "
            "(greater NYC metro). Pick a location within the map's usual range."
        )
        return

    pickup = st.session_state.get(PICKUP_KEY)
    dropoff = st.session_state.get(DROPOFF_KEY)

    if pickup is None:
        st.session_state[PICKUP_KEY] = (lat, lon)
    elif dropoff is None:
        st.session_state[DROPOFF_KEY] = (lat, lon)
    else:
        # both already set -> start a new trip from this click
        st.session_state[PICKUP_KEY] = (lat, lon)
        st.session_state[DROPOFF_KEY] = None


def _build_map() -> folium.Map:
    pickup = st.session_state.get(PICKUP_KEY)
    dropoff = st.session_state.get(DROPOFF_KEY)

    center = pickup if pickup else (MAP_DEFAULT_LAT, MAP_DEFAULT_LON)
    fmap = folium.Map(
        location=center,
        zoom_start=MAP_DEFAULT_ZOOM,
        tiles="CartoDB positron",  # light basemap to match the white Uber-style theme
    )

    if pickup:
        folium.Marker(
            location=pickup,
            tooltip="Pickup",
            icon=folium.Icon(color="black", icon="circle", prefix="fa"),
        ).add_to(fmap)

    if dropoff:
        folium.Marker(
            location=dropoff,
            tooltip="Drop-off",
            icon=folium.Icon(color="gray", icon="square", prefix="fa"),
        ).add_to(fmap)

    if pickup and dropoff:
        folium.PolyLine(
            locations=[pickup, dropoff],
            color=THEME.text_primary,
            weight=4,
            opacity=0.85,
            dash_array="6,8",
        ).add_to(fmap)

    return fmap


def render_map() -> tuple[tuple[float, float] | None, tuple[float, float] | None]:
    """Render the map, handle clicks, and return (pickup, dropoff)."""
    st.session_state.setdefault(PICKUP_KEY, None)
    st.session_state.setdefault(DROPOFF_KEY, None)

    pickup = st.session_state[PICKUP_KEY]
    dropoff = st.session_state[DROPOFF_KEY]

    if pickup is None:
        st.caption("Click the map to set your pickup location.")
    elif dropoff is None:
        st.caption("Now click to set your drop-off location.")
    else:
        st.caption("Trip ready. Click anywhere to start a new trip.")

    fmap = _build_map()
    map_state = st_folium(
        fmap,
        height=460,
        width=None,
        use_container_width=True,
        returned_objects=["last_clicked"],
        key="trip_map",
    )

    clicked = map_state.get("last_clicked") if map_state else None
    if clicked:
        lat, lon = clicked["lat"], clicked["lng"]
        last_processed = st.session_state.get("_last_map_click")
        if last_processed != (lat, lon):
            st.session_state["_last_map_click"] = (lat, lon)
            _handle_click(lat, lon)
            st.rerun()

    col_a, col_b, col_reset = st.columns([2, 2, 1])
    with col_a:
        if pickup:
            st.caption(f"Pickup: `{pickup[0]:.5f}, {pickup[1]:.5f}`")
    with col_b:
        if dropoff:
            st.caption(f"Drop-off: `{dropoff[0]:.5f}, {dropoff[1]:.5f}`")
    with col_reset:
        if st.button("Reset trip", use_container_width=True):
            st.session_state[PICKUP_KEY] = None
            st.session_state[DROPOFF_KEY] = None
            st.session_state["_last_map_click"] = None
            st.rerun()

    return pickup, dropoff
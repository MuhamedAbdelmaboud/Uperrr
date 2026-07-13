"""Interactive map: click for pickup, then drop-off."""
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
        st.warning("That location is outside the NYC metro area. Pick a point on the map.")
        return

    pickup = st.session_state.get(PICKUP_KEY)
    dropoff = st.session_state.get(DROPOFF_KEY)

    if pickup is None:
        st.session_state[PICKUP_KEY] = (lat, lon)
    elif dropoff is None:
        st.session_state[DROPOFF_KEY] = (lat, lon)
    else:
        st.session_state[PICKUP_KEY] = (lat, lon)
        st.session_state[DROPOFF_KEY] = None


def _marker(lat: float, lon: float, color: str, tooltip: str) -> folium.CircleMarker:
    return folium.CircleMarker(
        location=(lat, lon),
        radius=8,
        color=color,
        weight=3,
        fill=True,
        fill_color=color,
        fill_opacity=1.0,
        tooltip=tooltip,
    )


def _build_map() -> folium.Map:
    pickup = st.session_state.get(PICKUP_KEY)
    dropoff = st.session_state.get(DROPOFF_KEY)
    center = pickup if pickup else (MAP_DEFAULT_LAT, MAP_DEFAULT_LON)

    fmap = folium.Map(
        location=center,
        zoom_start=MAP_DEFAULT_ZOOM,
        tiles="CartoDB positron",
    )

    if pickup:
        _marker(pickup[0], pickup[1], THEME.pickup, "Pickup").add_to(fmap)
    if dropoff:
        _marker(dropoff[0], dropoff[1], THEME.dropoff, "Drop-off").add_to(fmap)
    if pickup and dropoff:
        folium.PolyLine(
            locations=[pickup, dropoff],
            color=THEME.map_route,
            weight=4,
            opacity=0.85,
        ).add_to(fmap)

    return fmap


def _render_locations(pickup, dropoff) -> None:
    if not pickup and not dropoff:
        return

    parts = []
    if pickup:
        parts.append(
            f"""
            <div class="location-row">
                <div class="location-dot pickup"></div>
                <div>
                    <div class="location-label">Pickup</div>
                    <div class="location-coords">{pickup[0]:.5f}, {pickup[1]:.5f}</div>
                </div>
            </div>
            """
        )
    if pickup and dropoff:
        parts.append('<div class="location-divider"></div>')
    if dropoff:
        parts.append(
            f"""
            <div class="location-row">
                <div class="location-dot dropoff"></div>
                <div>
                    <div class="location-label">Drop-off</div>
                    <div class="location-coords">{dropoff[0]:.5f}, {dropoff[1]:.5f}</div>
                </div>
            </div>
            """
        )

    st.markdown("".join(parts), unsafe_allow_html=True)


def render_map() -> tuple[tuple[float, float] | None, tuple[float, float] | None]:
    st.session_state.setdefault(PICKUP_KEY, None)
    st.session_state.setdefault(DROPOFF_KEY, None)

    pickup = st.session_state[PICKUP_KEY]
    dropoff = st.session_state[DROPOFF_KEY]

    if pickup is None:
        hint = "Tap the map to set your pickup location"
    elif dropoff is None:
        hint = "Now tap to set your drop-off location"
    else:
        hint = "Route ready -- tap anywhere to start a new trip"

    st.markdown(f'<div class="map-card"><p class="map-hint">{hint}</p>', unsafe_allow_html=True)
    _render_locations(pickup, dropoff)

    map_state = st_folium(
        _build_map(),
        height=500,
        width="stretch",
        returned_objects=["last_clicked"],
        key="trip_map",
    )

    clicked = map_state.get("last_clicked") if map_state else None
    if clicked:
        lat, lon = clicked["lat"], clicked["lng"]
        last = st.session_state.get("_last_map_click")
        if last != (lat, lon):
            st.session_state["_last_map_click"] = (lat, lon)
            _handle_click(lat, lon)
            st.rerun()

    if st.button("Clear route", width="stretch"):
        st.session_state[PICKUP_KEY] = None
        st.session_state[DROPOFF_KEY] = None
        st.session_state["_last_map_click"] = None
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    return pickup, dropoff

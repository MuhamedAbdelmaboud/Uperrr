"""Trip detail controls: passenger count, ride type, pickup date/time.

Renders inline (NOT in st.sidebar) so the layout matches a real ride-hailing
app: map dominant, controls in a panel alongside it. Filename kept as
sidebar.py to match the established module contract in main.py.
"""
from datetime import date, datetime, time

import streamlit as st

from config import MAX_PASSENGERS, MIN_PASSENGERS, RIDE_TYPES


def render_sidebar() -> dict:
    """Render trip-detail inputs and return the collected values."""
    st.markdown("**Passengers**")
    passenger_count = st.slider(
        "Passengers", min_value=MIN_PASSENGERS, max_value=MAX_PASSENGERS, value=1,
        label_visibility="collapsed",
    )

    st.markdown("**Ride type**")
    ride_labels = [rt.label for rt in RIDE_TYPES]
    chosen_idx = st.radio(
        "Ride type", options=range(len(RIDE_TYPES)),
        format_func=lambda i: ride_labels[i], label_visibility="collapsed",
        horizontal=True,
    )
    ride_type = RIDE_TYPES[chosen_idx]

    if passenger_count > ride_type.capacity:
        st.warning(
            f"{ride_type.label} seats up to {ride_type.capacity}. "
            "Pick a bigger ride type or reduce passengers."
        )

    st.markdown("**Pickup time**")
    col_date, col_time = st.columns(2)
    with col_date:
        trip_date = st.date_input("Date", value=date.today(), label_visibility="collapsed")
    with col_time:
        trip_time = st.time_input(
            "Time", value=time(hour=datetime.now().hour), label_visibility="collapsed",
        )

    return {
        "passenger_count": passenger_count,
        "ride_type": ride_type,
        "pickup_datetime": datetime.combine(trip_date, trip_time),
    }
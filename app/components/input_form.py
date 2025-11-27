"""Input form component for Streamlit."""

import streamlit as st
from app.data.constants import (
    STATES,
    FUEL_TYPES,
    OWNER_OPTIONS,
    BRAND_OPTIONS,
    TRANSMISSION_OPTIONS,
    CONDITION_OPTIONS,
    ACCIDENT_OPTIONS,
    SERVICE_OPTIONS,
    INSURANCE_OPTIONS,
    YEARS,
)


def render_input_form() -> dict:
    """
    Render the input form and return collected values.

    Returns dict with all input values.
    """
    st.subheader("Car Details")

    # Required inputs
    col1, col2 = st.columns(2)

    with col1:
        ex_showroom = st.number_input(
            "Ex-Showroom Price (Rs.)",
            min_value=100000,
            max_value=50000000,
            value=1500000,
            step=50000,
            help="Original ex-showroom price when new",
        )

        year = st.selectbox(
            "Year of Manufacture",
            options=YEARS,
            index=2,
            help="Manufacturing year of the car",
        )

        km = st.number_input(
            "Kilometers Driven",
            min_value=0,
            max_value=500000,
            value=40000,
            step=1000,
            help="Total kilometers on odometer",
        )

        fuel_type = st.selectbox(
            "Fuel Type",
            options=FUEL_TYPES,
            help="Fuel/power type of the car",
        )

    with col2:
        state = st.selectbox(
            "Registration State",
            options=STATES,
            index=0,
            help="State where car was registered",
        )

        owner = st.selectbox(
            "Owner Number",
            options=OWNER_OPTIONS,
            help="Which owner are you buying from?",
        )

        asking_price = st.number_input(
            "Asking Price (Rs.)",
            min_value=50000,
            max_value=50000000,
            value=1000000,
            step=25000,
            help="Price the seller is asking",
        )

        insurance_status = st.selectbox(
            "Insurance Status",
            options=INSURANCE_OPTIONS,
            help="Is current insurance valid?",
        )

    # Advanced options (collapsed by default)
    with st.expander("Advanced Options", expanded=False):
        adv_col1, adv_col2 = st.columns(2)

        with adv_col1:
            brand = st.selectbox(
                "Brand",
                options=BRAND_OPTIONS,
                index=BRAND_OPTIONS.index("Other"),
                help="Car manufacturer (affects depreciation rate)",
            )

            transmission = st.selectbox(
                "Transmission",
                options=TRANSMISSION_OPTIONS,
                help="Type of gearbox",
            )

            body_condition = st.selectbox(
                "Body Condition",
                options=CONDITION_OPTIONS,
                index=1,  # Default to "Good"
                help="Overall exterior/interior condition",
            )

        with adv_col2:
            accident_history = st.selectbox(
                "Accident History",
                options=ACCIDENT_OPTIONS,
                help="Known accident history",
            )

            service_history = st.selectbox(
                "Service History",
                options=SERVICE_OPTIONS,
                index=2,  # Default to "Unknown"
                help="Service record availability",
            )

            commercial_use = st.checkbox(
                "Commercial Use (Taxi/Fleet)",
                value=False,
                help="Was the car used commercially?",
            )

            new_gen_available = st.checkbox(
                "New Generation Available",
                value=False,
                help="Is a newer generation model available?",
            )

    return {
        "ex_showroom": ex_showroom,
        "year": year,
        "km": km,
        "fuel_type": fuel_type,
        "state": state,
        "owner": owner,
        "asking_price": asking_price,
        "insurance_status": insurance_status,
        "brand": brand,
        "transmission": transmission,
        "body_condition": body_condition,
        "accident_history": accident_history,
        "service_history": service_history,
        "commercial_use": commercial_use,
        "new_gen_available": new_gen_available,
    }

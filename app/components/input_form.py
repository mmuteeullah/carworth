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

# Default values for advanced options
ADVANCED_DEFAULTS = {
    "brand": "Other",
    "transmission": "Manual",
    "body_condition": "Good",
    "accident_history": "None",
    "service_history": "Unknown",
    "commercial_use": False,
    "new_gen_available": False,
}


def _render_car_inputs(key_prefix: str = "", label: str = "Car Details") -> dict:
    """
    Render input fields for a single car.

    Args:
        key_prefix: Prefix for widget keys (for comparison mode)
        label: Section label

    Returns dict with all input values.
    """
    st.subheader(label)

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
            key=f"{key_prefix}ex_showroom",
        )

        year = st.selectbox(
            "Year of Manufacture",
            options=YEARS,
            index=2,
            help="Manufacturing year of the car",
            key=f"{key_prefix}year",
        )

        km = st.number_input(
            "Kilometers Driven",
            min_value=0,
            max_value=500000,
            value=40000,
            step=1000,
            help="Total kilometers on odometer",
            key=f"{key_prefix}km",
        )

        fuel_type = st.selectbox(
            "Fuel Type",
            options=FUEL_TYPES,
            help="Fuel/power type of the car",
            key=f"{key_prefix}fuel_type",
        )

    with col2:
        state = st.selectbox(
            "Registration State",
            options=STATES,
            index=0,
            help="State where car was registered",
            key=f"{key_prefix}state",
        )

        owner = st.selectbox(
            "Owner Number",
            options=OWNER_OPTIONS,
            help="Which owner are you buying from?",
            key=f"{key_prefix}owner",
        )

        asking_price = st.number_input(
            "Asking Price (Rs.)",
            min_value=50000,
            max_value=50000000,
            value=1000000,
            step=25000,
            help="Price the seller is asking",
            key=f"{key_prefix}asking_price",
        )

        insurance_status = st.selectbox(
            "Insurance Status",
            options=INSURANCE_OPTIONS,
            help="Is current insurance valid?",
            key=f"{key_prefix}insurance_status",
        )

    # Custom road tax option
    use_custom_road_tax = st.checkbox(
        "Use custom road tax rate",
        value=False,
        help="Override the default road tax rate if you know the exact rate for your state/vehicle",
        key=f"{key_prefix}use_custom_road_tax",
    )

    custom_road_tax_rate = None
    if use_custom_road_tax:
        custom_road_tax_rate = st.number_input(
            "Custom Road Tax Rate (%)",
            min_value=0.0,
            max_value=30.0,
            value=10.0,
            step=0.5,
            help="Enter road tax percentage (e.g., 12 for 12%)",
            key=f"{key_prefix}custom_road_tax_rate",
        ) / 100.0

    # Advanced options
    with st.expander("Advanced Options (Edge Cases)", expanded=False):
        st.caption(
            "These adjustments are for special situations. "
            "The basic formula works for 80% of cases."
        )

        adv_col1, adv_col2 = st.columns(2)

        with adv_col1:
            brand = st.selectbox(
                "Brand",
                options=BRAND_OPTIONS,
                index=BRAND_OPTIONS.index("Other"),
                help="Affects depreciation: Maruti/Toyota hold value better, Skoda/VW depreciate faster",
                key=f"{key_prefix}brand",
            )

            transmission = st.selectbox(
                "Transmission",
                options=TRANSMISSION_OPTIONS,
                help="DCT/DSG adds +5% depreciation (reliability concerns), AMT adds +2%",
                key=f"{key_prefix}transmission",
            )

            body_condition = st.selectbox(
                "Body Condition",
                options=CONDITION_OPTIONS,
                index=1,
                help="Excellent: -2%, Good: 0%, Average: +2%, Poor: +5%",
                key=f"{key_prefix}body_condition",
            )

        with adv_col2:
            accident_history = st.selectbox(
                "Accident History",
                options=ACCIDENT_OPTIONS,
                help="Minor accident: +10%, Major accident: +20%",
                key=f"{key_prefix}accident_history",
            )

            service_history = st.selectbox(
                "Service History",
                options=SERVICE_OPTIONS,
                index=2,
                help="Full authorized: -2%, Partial: 0%, Unknown: +3%",
                key=f"{key_prefix}service_history",
            )

            commercial_use = st.checkbox(
                "Commercial Use (Taxi/Fleet)",
                value=False,
                help="Adds +15% depreciation for taxi/fleet vehicles",
                key=f"{key_prefix}commercial_use",
            )

            new_gen_available = st.checkbox(
                "New Generation Available",
                value=False,
                help="Adds +5% if newer model generation has launched",
                key=f"{key_prefix}new_gen_available",
            )

    # Check if any advanced option was changed from default
    use_advanced = (
        brand != ADVANCED_DEFAULTS["brand"]
        or transmission != ADVANCED_DEFAULTS["transmission"]
        or body_condition != ADVANCED_DEFAULTS["body_condition"]
        or accident_history != ADVANCED_DEFAULTS["accident_history"]
        or service_history != ADVANCED_DEFAULTS["service_history"]
        or commercial_use != ADVANCED_DEFAULTS["commercial_use"]
        or new_gen_available != ADVANCED_DEFAULTS["new_gen_available"]
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
        "custom_road_tax_rate": custom_road_tax_rate,
        "brand": brand,
        "transmission": transmission,
        "body_condition": body_condition,
        "accident_history": accident_history,
        "service_history": service_history,
        "commercial_use": commercial_use,
        "new_gen_available": new_gen_available,
        "use_advanced": use_advanced,
    }


def render_input_form() -> dict:
    """
    Render the input form and return collected values.

    Returns dict with all input values plus 'use_advanced' flag.
    """
    return _render_car_inputs(key_prefix="single_", label="Car Details")


def render_comparison_form() -> tuple[dict, dict]:
    """
    Render comparison mode with two side-by-side car input forms.

    Returns tuple of (car1_inputs, car2_inputs)
    """
    col1, col2 = st.columns(2)

    with col1:
        car1 = _render_car_inputs(key_prefix="car1_", label="Car 1")

    with col2:
        car2 = _render_car_inputs(key_prefix="car2_", label="Car 2")

    return car1, car2

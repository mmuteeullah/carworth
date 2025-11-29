"""Input form component with shadcn-ui components."""

import streamlit as st
import streamlit_shadcn_ui as ui
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
    "engine_cc": None,
    "length_mm": None,
}


def _render_car_inputs(key_prefix: str = "", label: str = "Car Details") -> dict:
    """
    Render input fields for a single car using shadcn components.

    Args:
        key_prefix: Prefix for widget keys (for comparison mode)
        label: Section label

    Returns dict with all input values.
    """
    st.markdown(f"### {label}")

    # Required inputs - Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ex-Showroom Price (₹)**")
        ex_showroom_str = ui.input(
            default_value="1500000",
            type="number",
            placeholder="Ex-showroom price when new",
            key=f"{key_prefix}ex_showroom",
        )
        ex_showroom = int(ex_showroom_str) if ex_showroom_str else 1500000

        st.markdown("**Year of Manufacture**")
        year = ui.select(
            options=[str(y) for y in YEARS],
            key=f"{key_prefix}year",
        )
        year = int(year) if year else YEARS[2]

        st.markdown("**Kilometers Driven**")
        km_str = ui.input(
            default_value="40000",
            type="number",
            placeholder="Total km on odometer",
            key=f"{key_prefix}km",
        )
        km = int(km_str) if km_str else 40000

        st.markdown("**Fuel Type**")
        fuel_type = ui.select(
            options=FUEL_TYPES,
            key=f"{key_prefix}fuel_type",
        )
        fuel_type = fuel_type or FUEL_TYPES[0]

    with col2:
        st.markdown("**Registration State**")
        state = ui.select(
            options=STATES,
            key=f"{key_prefix}state",
        )
        state = state or STATES[0]

        st.markdown("**Owner Number**")
        owner = ui.select(
            options=OWNER_OPTIONS,
            key=f"{key_prefix}owner",
        )
        owner = owner or OWNER_OPTIONS[0]

        st.markdown("**Asking Price (₹)**")
        asking_price_str = ui.input(
            default_value="1000000",
            type="number",
            placeholder="Seller's asking price",
            key=f"{key_prefix}asking_price",
        )
        asking_price = int(asking_price_str) if asking_price_str else 1000000

        st.markdown("**Insurance Status**")
        insurance_status = ui.select(
            options=INSURANCE_OPTIONS,
            key=f"{key_prefix}insurance_status",
        )
        insurance_status = insurance_status or INSURANCE_OPTIONS[0]

    # Custom road tax option
    st.markdown("")  # Spacer
    use_custom_road_tax = ui.switch(
        default_checked=False,
        label="Use custom road tax rate",
        key=f"{key_prefix}use_custom_road_tax",
    )

    custom_road_tax_rate = None
    if use_custom_road_tax:
        st.markdown("**Custom Road Tax Rate (%)**")
        custom_rate_str = ui.input(
            default_value="10",
            type="number",
            placeholder="e.g., 12 for 12%",
            key=f"{key_prefix}custom_road_tax_rate",
        )
        custom_road_tax_rate = float(custom_rate_str) / 100.0 if custom_rate_str else 0.10

    # Advanced options
    st.markdown("")  # Spacer
    with st.expander("⚙️ Advanced Options (Edge Cases)", expanded=False):
        st.caption(
            "These adjustments are for special situations. "
            "The basic formula works for 80% of cases."
        )

        adv_col1, adv_col2 = st.columns(2)

        with adv_col1:
            st.markdown("**Brand**")
            brand = ui.select(
                options=BRAND_OPTIONS,
                key=f"{key_prefix}brand",
            )
            brand = brand or "Other"

            st.markdown("**Transmission**")
            transmission = ui.select(
                options=TRANSMISSION_OPTIONS,
                key=f"{key_prefix}transmission",
            )
            transmission = transmission or "Manual"

            st.markdown("**Body Condition**")
            body_condition = ui.select(
                options=CONDITION_OPTIONS,
                key=f"{key_prefix}body_condition",
            )
            body_condition = body_condition or "Good"

        with adv_col2:
            st.markdown("**Accident History**")
            accident_history = ui.select(
                options=ACCIDENT_OPTIONS,
                key=f"{key_prefix}accident_history",
            )
            accident_history = accident_history or "None"

            st.markdown("**Service History**")
            service_history = ui.select(
                options=SERVICE_OPTIONS,
                key=f"{key_prefix}service_history",
            )
            service_history = service_history or "Unknown"

            st.markdown("")  # Spacer
            commercial_use = ui.switch(
                default_checked=False,
                label="Commercial Use (Taxi/Fleet)",
                key=f"{key_prefix}commercial_use",
            )

            new_gen_available = ui.switch(
                default_checked=False,
                label="New Generation Available",
                key=f"{key_prefix}new_gen_available",
            )

        # GST Classification section
        st.markdown("---")
        st.markdown("**🧾 GST Classification (Optional)**")
        st.caption(
            "Provide engine CC and length to accurately determine GST rate. "
            "Small cars (Petrol ≤1200cc / Diesel ≤1500cc AND ≤4000mm) get 18% GST, "
            "larger vehicles get 40% GST."
        )

        gst_col1, gst_col2 = st.columns(2)

        with gst_col1:
            st.markdown("**Engine Capacity (CC)**")
            engine_cc_str = ui.input(
                default_value="",
                type="number",
                placeholder="e.g., 1197",
                key=f"{key_prefix}engine_cc",
            )
            engine_cc = int(engine_cc_str) if engine_cc_str and engine_cc_str.strip() else None

        with gst_col2:
            st.markdown("**Vehicle Length (mm)**")
            length_mm_str = ui.input(
                default_value="",
                type="number",
                placeholder="e.g., 3995",
                key=f"{key_prefix}length_mm",
            )
            length_mm = int(length_mm_str) if length_mm_str and length_mm_str.strip() else None

        # Show GST info hint
        if fuel_type == "Electric":
            st.info("⚡ Electric vehicles always qualify for 5% GST regardless of size")
        elif engine_cc and length_mm:
            from app.data.gst import classify_gst_category
            gst_info = classify_gst_category(fuel_type, engine_cc, length_mm)
            if gst_info["category"] == "small":
                st.success(f"✅ {gst_info['category_name']} - {gst_info['reason']}")
            else:
                st.warning(f"⚠️ {gst_info['category_name']} - {gst_info['reason']}")

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
        "commercial_use": commercial_use or False,
        "new_gen_available": new_gen_available or False,
        "use_advanced": use_advanced,
        "engine_cc": engine_cc,
        "length_mm": length_mm,
    }


def render_input_form() -> dict:
    """
    Render the input form and return collected values.

    Returns dict with all input values plus 'use_advanced' flag.
    """
    return _render_car_inputs(key_prefix="single_", label="📝 Car Details")


def render_comparison_form() -> tuple[dict, dict]:
    """
    Render comparison mode with two side-by-side car input forms.

    Returns tuple of (car1_inputs, car2_inputs)
    """
    col1, col2 = st.columns(2)

    with col1:
        car1 = _render_car_inputs(key_prefix="car1_", label="🚗 Car 1")

    with col2:
        car2 = _render_car_inputs(key_prefix="car2_", label="🚙 Car 2")

    return car1, car2

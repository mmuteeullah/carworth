"""Calculation breakdown component."""

import streamlit as st
from app.utils.formatters import (
    format_currency,
    format_currency_lakhs,
    format_percentage,
    format_km,
)


def render_breakdown(
    on_road_data: dict,
    depreciation_data: dict,
    fair_value_data: dict,
) -> None:
    """
    Render detailed calculation breakdown.

    Args:
        on_road_data: Dict from calculate_on_road_price()
        depreciation_data: Dict from calculate_total_depreciation()
        fair_value_data: Dict from calculate_complete_fair_value()
    """
    st.subheader("Calculation Breakdown")

    # On-Road Price Section
    with st.expander("Step 1: On-Road Price Calculation", expanded=True):
        st.markdown("**Original On-Road Price Components:**")

        data = [
            ("Ex-Showroom Price", on_road_data["ex_showroom"]),
            (f"Road Tax ({format_percentage(on_road_data['road_tax_rate'])})", on_road_data["road_tax"]),
            ("Insurance (Estimated)", on_road_data["insurance"]),
            ("Fixed Charges (Reg + HSRP + FasTag)", on_road_data["fixed_charges"]),
        ]

        for label, value in data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(label)
            with col2:
                st.text(format_currency_lakhs(value))

        st.divider()
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Total On-Road Price**")
        with col2:
            st.markdown(f"**{format_currency_lakhs(on_road_data['on_road_price'])}**")

    # Depreciation Section
    with st.expander("Step 2: Depreciation Calculation", expanded=True):
        st.markdown("**Depreciation Components:**")

        age = depreciation_data["age"]
        brand_mult = depreciation_data["brand_multiplier"]

        data = [
            (f"Life Depreciation ({age} years)", depreciation_data["life_depreciation"]),
            (f"Brand Multiplier", f"x{brand_mult:.2f}"),
            ("After Brand Adjustment", depreciation_data["branded_life_depreciation"]),
            ("Ownership Premium", depreciation_data["ownership_premium"]),
            ("Mileage Adjustment", depreciation_data["mileage_adjustment"]),
            ("Transmission Adjustment", depreciation_data["transmission_adjustment"]),
        ]

        for label, value in data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(label)
            with col2:
                if isinstance(value, str):
                    st.text(value)
                else:
                    st.text(format_percentage(value))

        # Condition adjustments
        cond = depreciation_data["condition_adjustments"]
        if cond["total"] != 0:
            st.markdown("**Condition Adjustments:**")
            if cond["body"] != 0:
                st.text(f"  Body Condition: {format_percentage(cond['body'])}")
            if cond["accident"] != 0:
                st.text(f"  Accident History: {format_percentage(cond['accident'])}")
            if cond["service"] != 0:
                st.text(f"  Service History: {format_percentage(cond['service'])}")
            if cond["commercial"] != 0:
                st.text(f"  Commercial Use: {format_percentage(cond['commercial'])}")
            if cond["new_gen"] != 0:
                st.text(f"  New Gen Available: {format_percentage(cond['new_gen'])}")

        st.divider()

        col1, col2 = st.columns([3, 1])
        with col1:
            label = "**Total Depreciation**"
            if depreciation_data["is_capped"]:
                label += " (Capped)"
            st.markdown(label)
        with col2:
            st.markdown(f"**{format_percentage(depreciation_data['total_capped'])}**")

        if depreciation_data["is_capped"]:
            st.caption(
                f"Raw depreciation was {format_percentage(depreciation_data['total_raw'])}, "
                "capped at 85% (minimum 15% value retention)"
            )

    # Fair Value Section
    with st.expander("Step 3: Fair Value Calculation", expanded=True):
        st.markdown("**Final Calculation:**")

        on_road = on_road_data["on_road_price"]
        dep_rate = depreciation_data["total_capped"]

        st.markdown(
            f"Fair Value = On-Road Price x (1 - Depreciation)  \n"
            f"Fair Value = {format_currency_lakhs(on_road)} x (1 - {format_percentage(dep_rate)})  \n"
            f"Fair Value = {format_currency_lakhs(on_road)} x {1 - dep_rate:.2f}"
        )

        st.divider()

        col1, col2 = st.columns([3, 1])
        with col1:
            st.text("Base Fair Value")
        with col2:
            st.text(format_currency_lakhs(fair_value_data["base_fair_value"]))

        if fair_value_data["insurance_deduction"] > 0:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text("Insurance Deduction (Expired)")
            with col2:
                st.text(f"- {format_currency_lakhs(fair_value_data['insurance_deduction'])}")

        st.divider()

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Final Fair Value**")
        with col2:
            st.markdown(f"**{format_currency_lakhs(fair_value_data['fair_value'])}**")

        st.caption(
            f"Fair Value Range: {format_currency_lakhs(fair_value_data['fair_value_min'])} "
            f"- {format_currency_lakhs(fair_value_data['fair_value_max'])} (+/- 5%)"
        )

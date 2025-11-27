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

    use_advanced = fair_value_data.get("using_advanced", False)

    # On-Road Price Section
    with st.expander("Step 1: On-Road Price Calculation", expanded=True):
        st.markdown("**Original On-Road Price Components:**")

        road_tax_rate = on_road_data["road_tax_rate"]
        data = [
            ("Ex-Showroom Price", on_road_data["ex_showroom"]),
            (f"Road Tax ({format_percentage(road_tax_rate)})", on_road_data["road_tax"]),
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

        # Road tax disclaimer - different message for custom vs default
        is_custom_rate = on_road_data.get("is_custom_rate", False)
        if is_custom_rate:
            default_rate = on_road_data.get("default_road_tax_rate", road_tax_rate)
            st.success(
                f"Using **custom road tax rate: {format_percentage(road_tax_rate)}** "
                f"(Default for this state: {format_percentage(default_rate)})"
            )
        else:
            st.warning(
                f"Road tax rate used: **{format_percentage(road_tax_rate)}** "
                f"(Static data from 2024-25 government sources. "
                f"Actual rates may vary. Verify with your local RTO.)"
            )

    # Depreciation Section
    with st.expander("Step 2: Depreciation Calculation", expanded=True):
        age = depreciation_data["age"]
        life_years = depreciation_data.get("life_years", 15)

        # Basic Formula Section
        st.markdown("**Basic Formula** (Life + Ownership + Mileage)")
        st.caption(f"Life Depreciation = Age / {life_years} years")

        basic_data = [
            (f"Life Depreciation ({age} yrs / {life_years} yrs)", depreciation_data["life_depreciation"]),
            ("Ownership Premium", depreciation_data["ownership_premium"]),
            ("Mileage Adjustment", depreciation_data["mileage_adjustment"]),
        ]

        for label, value in basic_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(label)
            with col2:
                st.text(format_percentage(value))

        # Basic total
        st.divider()
        col1, col2 = st.columns([3, 1])
        with col1:
            basic_label = "**Basic Total**"
            if depreciation_data.get("basic_is_capped"):
                basic_label += " (Capped at 85%)"
            st.markdown(basic_label)
        with col2:
            st.markdown(f"**{format_percentage(depreciation_data['basic_capped'])}**")

        # Advanced adjustments (if used)
        if use_advanced:
            st.divider()
            st.markdown("**Edge Case Adjustments** (Advanced)")

            brand_mult = depreciation_data["brand_multiplier"]
            advanced_data = []

            # Only show non-zero adjustments
            if depreciation_data["brand_adjustment"] != 0:
                advanced_data.append((f"Brand Adjustment (x{brand_mult:.2f})", depreciation_data["brand_adjustment"]))

            if depreciation_data["transmission_adjustment"] != 0:
                advanced_data.append(("Transmission Risk", depreciation_data["transmission_adjustment"]))

            cond = depreciation_data["condition_adjustments"]
            if cond["body"] != 0:
                advanced_data.append(("Body Condition", cond["body"]))
            if cond["accident"] != 0:
                advanced_data.append(("Accident History", cond["accident"]))
            if cond["service"] != 0:
                advanced_data.append(("Service History", cond["service"]))
            if cond["commercial"] != 0:
                advanced_data.append(("Commercial Use", cond["commercial"]))
            if cond["new_gen"] != 0:
                advanced_data.append(("New Gen Available", cond["new_gen"]))

            if advanced_data:
                for label, value in advanced_data:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(label)
                    with col2:
                        st.text(format_percentage(value))

            # Advanced total
            st.divider()
            col1, col2 = st.columns([3, 1])
            with col1:
                adv_label = "**Advanced Total**"
                if depreciation_data.get("advanced_is_capped"):
                    adv_label += " (Capped at 85%)"
                st.markdown(adv_label)
            with col2:
                st.markdown(f"**{format_percentage(depreciation_data['advanced_capped'])}**")

            # Show difference
            diff = depreciation_data["advanced_capped"] - depreciation_data["basic_capped"]
            if diff != 0:
                st.caption(
                    f"Edge case adjustments add {format_percentage(abs(diff))} "
                    f"{'more' if diff > 0 else 'less'} depreciation"
                )

    # Fair Value Section
    with st.expander("Step 3: Fair Value Calculation", expanded=True):
        on_road = on_road_data["on_road_price"]

        if use_advanced:
            st.markdown("**Comparison: Basic vs Advanced**")

            col_b, col_a = st.columns(2)

            with col_b:
                st.markdown("*Basic Formula*")
                basic_dep = depreciation_data["basic_capped"]
                st.text(f"On-Road x (1 - {format_percentage(basic_dep)})")
                st.text(f"= {format_currency_lakhs(fair_value_data['basic_adjusted'])}")

            with col_a:
                st.markdown("*With Edge Cases*")
                adv_dep = depreciation_data["advanced_capped"]
                st.text(f"On-Road x (1 - {format_percentage(adv_dep)})")
                st.text(f"= {format_currency_lakhs(fair_value_data['advanced_adjusted'])}")

            st.divider()
            st.info("Using **Advanced Value** (with edge case adjustments)")

        else:
            st.markdown("**Final Calculation:**")
            dep_rate = depreciation_data["basic_capped"]

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

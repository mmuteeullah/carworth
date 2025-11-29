"""Calculation breakdown component with modern styling."""

import streamlit as st
import streamlit_shadcn_ui as ui
from app.utils.formatters import (
    format_currency,
    format_currency_lakhs,
    format_percentage,
    format_km,
)


def _render_row(label: str, value: str, is_total: bool = False) -> None:
    """Render a single breakdown row."""
    if is_total:
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: space-between;
                padding: 12px 0;
                border-top: 2px solid #4a5568;
                margin-top: 8px;
            ">
                <span style="font-weight: 700; color: #f3f4f6;">{label}</span>
                <span style="font-weight: 700; color: #60a5fa;">{value}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid #374151;
            ">
                <span style="color: #d1d5db;">{label}</span>
                <span style="color: #f3f4f6;">{value}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_breakdown(
    on_road_data: dict,
    depreciation_data: dict,
    fair_value_data: dict,
) -> None:
    """
    Render detailed calculation breakdown with modern accordion style.

    Args:
        on_road_data: Dict from calculate_on_road_price()
        depreciation_data: Dict from calculate_total_depreciation()
        fair_value_data: Dict from calculate_complete_fair_value()
    """
    st.markdown("### 📐 Calculation Breakdown")

    use_advanced = fair_value_data.get("using_advanced", False)

    # Step 1: On-Road Price
    with st.expander("Step 1: On-Road Price Calculation", expanded=False):
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #1e3a5f 0%, #172554 100%);
                border-radius: 8px;
                padding: 12px 16px;
                margin-bottom: 16px;
            ">
                <span style="color: #93c5fd; font-size: 0.9rem;">
                    Original on-road price when car was new
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        road_tax_rate = on_road_data["road_tax_rate"]
        slab_info = on_road_data.get("slab_info", {})
        gst_info = on_road_data.get("gst_info", {})
        gst_breakdown = on_road_data.get("gst_breakdown", {})

        _render_row("Ex-Showroom Price", format_currency_lakhs(on_road_data["ex_showroom"]))

        # Show GST breakdown if available
        if gst_breakdown and gst_breakdown.get("gst_amount"):
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(147, 51, 234, 0.1);
                    border-left: 3px solid #9333ea;
                    padding: 10px 12px;
                    margin: 8px 0 12px 20px;
                    border-radius: 4px;
                    font-size: 0.85rem;
                ">
                    <div style="color: #c4b5fd; font-weight: 600; margin-bottom: 6px;">
                        🧾 GST Breakdown (included in Ex-Showroom)
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #ddd6fe; margin-bottom: 4px;">
                        <span>Base Price (before GST)</span>
                        <span>{format_currency_lakhs(gst_breakdown['base_price'])}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #ddd6fe; margin-bottom: 4px;">
                        <span>GST ({gst_breakdown['gst_percent']})</span>
                        <span>{format_currency_lakhs(gst_breakdown['gst_amount'])}</span>
                    </div>
                    <div style="color: #a78bfa; font-size: 0.8rem; margin-top: 6px;">
                        {gst_info.get('category_name', '')} - {gst_info.get('reason', '')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        _render_row(f"Road Tax ({format_percentage(road_tax_rate)})", format_currency_lakhs(on_road_data["road_tax"]))
        _render_row("Insurance (Estimated)", format_currency_lakhs(on_road_data["insurance"]))
        _render_row("RTO Charges (Reg + HSRP + FasTag + Misc)", format_currency_lakhs(on_road_data["fixed_charges"]))
        _render_row("Handling/Logistics", format_currency_lakhs(on_road_data.get("handling_charges", 0)))

        # Show TCS if applicable
        tcs = on_road_data.get("tcs", 0)
        if tcs > 0:
            _render_row("TCS (1% above ₹10L)", format_currency_lakhs(tcs))

        _render_row("Total On-Road Price", format_currency_lakhs(on_road_data["on_road_price"]), is_total=True)

        # Road tax slab explanation
        is_custom_rate = on_road_data.get("is_custom_rate", False)
        if is_custom_rate:
            default_rate = on_road_data.get("default_road_tax_rate", road_tax_rate)
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(34, 197, 94, 0.1);
                    border-left: 3px solid #22c55e;
                    padding: 8px 12px;
                    margin-top: 12px;
                    border-radius: 4px;
                    font-size: 0.85rem;
                    color: #86efac;
                ">
                    ✓ Using custom rate: {format_percentage(road_tax_rate)} (Default: {format_percentage(default_rate)})
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif slab_info:
            # Show slab info with explanation
            slab_range = slab_info.get("slab_range", "")
            reason = slab_info.get("reason", "")
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(59, 130, 246, 0.1);
                    border-left: 3px solid #3b82f6;
                    padding: 10px 12px;
                    margin-top: 12px;
                    border-radius: 4px;
                    font-size: 0.85rem;
                ">
                    <div style="color: #93c5fd; font-weight: 600; margin-bottom: 4px;">
                        📋 Tax Slab Applied: {slab_range}
                    </div>
                    <div style="color: #bfdbfe;">
                        {reason}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(245, 158, 11, 0.1);
                    border-left: 3px solid #f59e0b;
                    padding: 8px 12px;
                    margin-top: 8px;
                    border-radius: 4px;
                    font-size: 0.8rem;
                    color: #fcd34d;
                ">
                    ⚠️ Rates based on 2024-25 data. Verify with RTO for latest rates.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(245, 158, 11, 0.1);
                    border-left: 3px solid #f59e0b;
                    padding: 8px 12px;
                    margin-top: 12px;
                    border-radius: 4px;
                    font-size: 0.85rem;
                    color: #fcd34d;
                ">
                    ⚠️ Road tax: {format_percentage(road_tax_rate)} (2024-25 data, verify with RTO)
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Step 2: Depreciation
    with st.expander("Step 2: Depreciation Calculation", expanded=False):
        age = depreciation_data["age"]
        life_years = depreciation_data.get("life_years", 15)

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #7c2d12 0%, #431407 100%);
                border-radius: 8px;
                padding: 12px 16px;
                margin-bottom: 16px;
            ">
                <span style="color: #fed7aa; font-size: 0.9rem;">
                    Life Depreciation = Age / {life_years} years
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Basic Formula**")
        _render_row(f"Life Depreciation ({age} yrs / {life_years} yrs)", format_percentage(depreciation_data["life_depreciation"]))
        _render_row("Ownership Premium", format_percentage(depreciation_data["ownership_premium"]))
        _render_row("Mileage Adjustment", format_percentage(depreciation_data["mileage_adjustment"]))

        basic_label = "Basic Total"
        if depreciation_data.get("basic_is_capped"):
            basic_label += " (Capped at 85%)"
        _render_row(basic_label, format_percentage(depreciation_data["basic_capped"]), is_total=True)

        # Advanced adjustments
        if use_advanced:
            st.markdown("")  # Spacer
            st.markdown("**Edge Case Adjustments**")

            brand_mult = depreciation_data["brand_multiplier"]
            cond = depreciation_data["condition_adjustments"]

            if depreciation_data["brand_adjustment"] != 0:
                _render_row(f"Brand Adjustment (x{brand_mult:.2f})", format_percentage(depreciation_data["brand_adjustment"]))

            if depreciation_data["transmission_adjustment"] != 0:
                _render_row("Transmission Risk", format_percentage(depreciation_data["transmission_adjustment"]))

            if cond["body"] != 0:
                _render_row("Body Condition", format_percentage(cond["body"]))
            if cond["accident"] != 0:
                _render_row("Accident History", format_percentage(cond["accident"]))
            if cond["service"] != 0:
                _render_row("Service History", format_percentage(cond["service"]))
            if cond["commercial"] != 0:
                _render_row("Commercial Use", format_percentage(cond["commercial"]))
            if cond["new_gen"] != 0:
                _render_row("New Gen Available", format_percentage(cond["new_gen"]))

            adv_label = "Advanced Total"
            if depreciation_data.get("advanced_is_capped"):
                adv_label += " (Capped at 85%)"
            _render_row(adv_label, format_percentage(depreciation_data["advanced_capped"]), is_total=True)

            # Difference
            diff = depreciation_data["advanced_capped"] - depreciation_data["basic_capped"]
            if diff != 0:
                st.markdown(
                    f"""
                    <div style="
                        background-color: rgba(99, 102, 241, 0.1);
                        border-radius: 6px;
                        padding: 8px 12px;
                        margin-top: 12px;
                        font-size: 0.85rem;
                        color: #a5b4fc;
                        text-align: center;
                    ">
                        Edge cases add {format_percentage(abs(diff))} {'more' if diff > 0 else 'less'} depreciation
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Step 3: Fair Value
    with st.expander("Step 3: Fair Value Calculation", expanded=False):
        on_road = on_road_data["on_road_price"]

        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #065f46 0%, #064e3b 100%);
                border-radius: 8px;
                padding: 12px 16px;
                margin-bottom: 16px;
            ">
                <span style="color: #a7f3d0; font-size: 0.9rem;">
                    Fair Value = On-Road × (1 - Depreciation)
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if use_advanced:
            col_b, col_a = st.columns(2)

            with col_b:
                basic_dep = depreciation_data["basic_capped"]
                st.markdown("**Basic Formula**")
                st.markdown(
                    f"""
                    <div style="
                        background-color: #1f2937;
                        border-radius: 8px;
                        padding: 12px;
                        text-align: center;
                    ">
                        <div style="color: #9ca3af; font-size: 0.8rem;">
                            {format_currency_lakhs(on_road)} × (1 - {format_percentage(basic_dep)})
                        </div>
                        <div style="color: #f3f4f6; font-size: 1.2rem; font-weight: 600; margin-top: 4px;">
                            = {format_currency_lakhs(fair_value_data['basic_adjusted'])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_a:
                adv_dep = depreciation_data["advanced_capped"]
                st.markdown("**With Edge Cases**")
                st.markdown(
                    f"""
                    <div style="
                        background-color: #1e3a5f;
                        border-radius: 8px;
                        padding: 12px;
                        text-align: center;
                    ">
                        <div style="color: #93c5fd; font-size: 0.8rem;">
                            {format_currency_lakhs(on_road)} × (1 - {format_percentage(adv_dep)})
                        </div>
                        <div style="color: #f3f4f6; font-size: 1.2rem; font-weight: 600; margin-top: 4px;">
                            = {format_currency_lakhs(fair_value_data['advanced_adjusted'])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            dep_rate = depreciation_data["basic_capped"]
            st.markdown(
                f"""
                <div style="
                    background-color: #1f2937;
                    border-radius: 8px;
                    padding: 16px;
                    text-align: center;
                ">
                    <div style="color: #9ca3af; font-size: 0.9rem;">
                        {format_currency_lakhs(on_road)} × (1 - {format_percentage(dep_rate)}) = {format_currency_lakhs(on_road)} × {1 - dep_rate:.2f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("")  # Spacer

        _render_row("Base Fair Value", format_currency_lakhs(fair_value_data["base_fair_value"]))

        if fair_value_data["insurance_deduction"] > 0:
            _render_row("Insurance Deduction (Expired)", f"- {format_currency_lakhs(fair_value_data['insurance_deduction'])}")

        _render_row("Final Fair Value", format_currency_lakhs(fair_value_data["fair_value"]), is_total=True)

        st.markdown(
            f"""
            <div style="
                background-color: rgba(59, 130, 246, 0.1);
                border-radius: 6px;
                padding: 8px 12px;
                margin-top: 12px;
                font-size: 0.85rem;
                color: #93c5fd;
                text-align: center;
            ">
                Range: {format_currency_lakhs(fair_value_data['fair_value_min'])} - {format_currency_lakhs(fair_value_data['fair_value_max'])} (±5%)
            </div>
            """,
            unsafe_allow_html=True,
        )

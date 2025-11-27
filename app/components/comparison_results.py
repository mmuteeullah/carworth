"""Comparison results component for side-by-side car valuation."""

import streamlit as st
import streamlit_shadcn_ui as ui
from app.utils.formatters import format_currency_lakhs, format_percentage


def render_comparison_results(
    car1_data: dict,
    car2_data: dict,
) -> None:
    """
    Render comparison results for two cars side by side.

    Args:
        car1_data: Dict with fair_value_data, verdict_data, inputs for car 1
        car2_data: Dict with fair_value_data, verdict_data, inputs for car 2
    """
    st.markdown("### 📊 Comparison Results")

    col1, col2 = st.columns(2)

    # Car 1 Results
    with col1:
        st.markdown("#### Car 1")
        _render_single_result(car1_data, "car1")

    # Car 2 Results
    with col2:
        st.markdown("#### Car 2")
        _render_single_result(car2_data, "car2")

    # Comparison summary
    st.markdown("")  # Spacer
    _render_comparison_summary(car1_data, car2_data)


def _render_single_result(data: dict, key_prefix: str) -> None:
    """Render result card for a single car."""
    fair_value_data = data["fair_value_data"]
    verdict_data = data["verdict_data"]
    inputs = data["inputs"]
    depreciation_data = data["depreciation_data"]

    # Fair Value using metric card
    ui.metric_card(
        title="Fair Market Value",
        content=format_currency_lakhs(fair_value_data["fair_value"]),
        description=f"Range: {format_currency_lakhs(fair_value_data['fair_value_min'])} - {format_currency_lakhs(fair_value_data['fair_value_max'])}",
        key=f"{key_prefix}_metric_fv",
    )

    st.markdown("")  # Spacer

    # Verdict with color
    verdict = verdict_data["verdict"]
    color = verdict_data["color"]

    if color == "success":
        bg_color, text_color = "#22c55e", "#ffffff"
    elif color == "error":
        bg_color, text_color = "#ef4444", "#ffffff"
    else:
        bg_color, text_color = "#f59e0b", "#000000"

    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            color: {text_color};
            padding: 12px 16px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.1rem;
            font-weight: 700;
            margin: 8px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        ">
            {verdict}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key details
    st.markdown(
        f"""
        <div style="
            background-color: #1f2937;
            border-radius: 8px;
            padding: 12px;
            margin-top: 8px;
            font-size: 0.85rem;
        ">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #9ca3af;">Asking</span>
                <span style="color: #f3f4f6; font-weight: 500;">{format_currency_lakhs(inputs['asking_price'])}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #9ca3af;">Year</span>
                <span style="color: #f3f4f6; font-weight: 500;">{inputs['year']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #9ca3af;">Kilometers</span>
                <span style="color: #f3f4f6; font-weight: 500;">{inputs['km']:,} km</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #9ca3af;">Depreciation</span>
                <span style="color: #f3f4f6; font-weight: 500;">{format_percentage(depreciation_data['basic_capped'])}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_comparison_summary(car1_data: dict, car2_data: dict) -> None:
    """Render comparison summary between two cars."""
    st.markdown("### 🏆 Recommendation")

    car1_fv = car1_data["fair_value_data"]["fair_value"]
    car2_fv = car2_data["fair_value_data"]["fair_value"]
    car1_asking = car1_data["inputs"]["asking_price"]
    car2_asking = car2_data["inputs"]["asking_price"]

    # Calculate value scores (how much below asking price vs fair value)
    car1_value_gap = car1_fv - car1_asking  # Positive = good deal
    car2_value_gap = car2_fv - car2_asking

    car1_pct = (car1_value_gap / car1_fv) * 100 if car1_fv > 0 else 0
    car2_pct = (car2_value_gap / car2_fv) * 100 if car2_fv > 0 else 0

    col1, col2 = st.columns(2)

    with col1:
        direction1 = "below" if car1_value_gap > 0 else "above"
        color1 = "#22c55e" if car1_value_gap > 0 else "#ef4444"
        ui.metric_card(
            title="Car 1 Value Gap",
            content=format_currency_lakhs(car1_value_gap),
            description=f"{abs(car1_pct):.1f}% {direction1} fair value",
            key="metric_gap_car1",
        )

    with col2:
        direction2 = "below" if car2_value_gap > 0 else "above"
        color2 = "#22c55e" if car2_value_gap > 0 else "#ef4444"
        ui.metric_card(
            title="Car 2 Value Gap",
            content=format_currency_lakhs(car2_value_gap),
            description=f"{abs(car2_pct):.1f}% {direction2} fair value",
            key="metric_gap_car2",
        )

    st.markdown("")  # Spacer

    # Determine winner
    if car1_pct > car2_pct:
        winner = "Car 1"
        winner_color = "#22c55e"
    elif car2_pct > car1_pct:
        winner = "Car 2"
        winner_color = "#22c55e"
    else:
        winner = "Tie"
        winner_color = "#3b82f6"

    if winner != "Tie":
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {winner_color} 0%, {winner_color}dd 100%);
                color: white;
                padding: 16px 20px;
                border-radius: 12px;
                text-align: center;
                margin: 12px 0;
                box-shadow: 0 4px 14px rgba(0,0,0,0.2);
            ">
                <span style="font-size: 1.5rem;">🏆</span>
                <div style="font-size: 1.2rem; font-weight: 700; margin-top: 4px;">
                    {winner} is the better value
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {winner_color} 0%, {winner_color}dd 100%);
                color: white;
                padding: 16px 20px;
                border-radius: 12px;
                text-align: center;
                margin: 12px 0;
            ">
                <span style="font-size: 1.5rem;">⚖️</span>
                <div style="font-size: 1.1rem; font-weight: 600; margin-top: 4px;">
                    Both cars offer similar value
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Additional insights
    insights = []

    # Age comparison
    car1_year = car1_data["inputs"]["year"]
    car2_year = car2_data["inputs"]["year"]
    if car1_year != car2_year:
        newer = "Car 1" if car1_year > car2_year else "Car 2"
        insights.append(f"📅 {newer} is newer ({max(car1_year, car2_year)} vs {min(car1_year, car2_year)})")

    # Mileage comparison
    car1_km = car1_data["inputs"]["km"]
    car2_km = car2_data["inputs"]["km"]
    if abs(car1_km - car2_km) > 10000:
        lower = "Car 1" if car1_km < car2_km else "Car 2"
        insights.append(f"🛣️ {lower} has lower mileage ({min(car1_km, car2_km):,} vs {max(car1_km, car2_km):,} km)")

    # Depreciation comparison
    car1_dep = car1_data["depreciation_data"]["basic_capped"]
    car2_dep = car2_data["depreciation_data"]["basic_capped"]
    if abs(car1_dep - car2_dep) > 0.05:
        lower = "Car 1" if car1_dep < car2_dep else "Car 2"
        insights.append(f"📉 {lower} has less depreciation ({format_percentage(min(car1_dep, car2_dep))} vs {format_percentage(max(car1_dep, car2_dep))})")

    if insights:
        st.markdown("#### Key Differences")
        for insight in insights:
            st.markdown(
                f"""
                <div style="
                    background-color: #1f2937;
                    border-radius: 8px;
                    padding: 10px 14px;
                    margin: 6px 0;
                    font-size: 0.9rem;
                    color: #d1d5db;
                ">
                    {insight}
                </div>
                """,
                unsafe_allow_html=True,
            )

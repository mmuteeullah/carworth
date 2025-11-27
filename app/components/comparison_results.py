"""Comparison results component for side-by-side car valuation."""

import streamlit as st
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
    st.subheader("Comparison Results")

    col1, col2 = st.columns(2)

    # Car 1 Results
    with col1:
        st.markdown("### Car 1")
        _render_single_result(car1_data)

    # Car 2 Results
    with col2:
        st.markdown("### Car 2")
        _render_single_result(car2_data)

    # Comparison summary
    st.divider()
    _render_comparison_summary(car1_data, car2_data)


def _render_single_result(data: dict) -> None:
    """Render result card for a single car."""
    fair_value_data = data["fair_value_data"]
    verdict_data = data["verdict_data"]
    inputs = data["inputs"]

    # Fair Value
    st.metric(
        label="Fair Market Value",
        value=format_currency_lakhs(fair_value_data["fair_value"]),
    )
    st.caption(
        f"Range: {format_currency_lakhs(fair_value_data['fair_value_min'])} - "
        f"{format_currency_lakhs(fair_value_data['fair_value_max'])}"
    )

    # Verdict with color
    verdict = verdict_data["verdict"]
    color = verdict_data["color"]
    if color == "success":
        st.success(verdict)
    elif color == "warning":
        st.warning(verdict)
    else:
        st.error(verdict)

    # Key details
    st.caption(
        f"Asking: {format_currency_lakhs(inputs['asking_price'])} | "
        f"Year: {inputs['year']} | "
        f"KM: {inputs['km']:,}"
    )

    # Depreciation
    depreciation_data = data["depreciation_data"]
    st.caption(f"Total Depreciation: {format_percentage(depreciation_data['basic_capped'])}")


def _render_comparison_summary(car1_data: dict, car2_data: dict) -> None:
    """Render comparison summary between two cars."""
    st.markdown("### Recommendation")

    car1_fv = car1_data["fair_value_data"]["fair_value"]
    car2_fv = car2_data["fair_value_data"]["fair_value"]
    car1_asking = car1_data["inputs"]["asking_price"]
    car2_asking = car2_data["inputs"]["asking_price"]

    # Calculate value scores (how much below asking price vs fair value)
    car1_value_gap = car1_fv - car1_asking  # Positive = good deal
    car2_value_gap = car2_fv - car2_asking

    car1_pct = (car1_value_gap / car1_fv) * 100 if car1_fv > 0 else 0
    car2_pct = (car2_value_gap / car2_fv) * 100 if car2_fv > 0 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Car 1 Value Gap",
            value=format_currency_lakhs(car1_value_gap),
            delta=f"{car1_pct:.1f}% {'below' if car1_value_gap > 0 else 'above'} fair value",
            delta_color="normal" if car1_value_gap > 0 else "inverse",
        )

    with col2:
        st.metric(
            label="Car 2 Value Gap",
            value=format_currency_lakhs(car2_value_gap),
            delta=f"{car2_pct:.1f}% {'below' if car2_value_gap > 0 else 'above'} fair value",
            delta_color="normal" if car2_value_gap > 0 else "inverse",
        )

    with col3:
        # Determine winner
        if car1_pct > car2_pct:
            winner = "Car 1"
            reason = "better value for money"
        elif car2_pct > car1_pct:
            winner = "Car 2"
            reason = "better value for money"
        else:
            winner = "Tie"
            reason = "similar value proposition"

        if winner != "Tie":
            st.success(f"**{winner}** is the {reason}")
        else:
            st.info(f"Both cars offer {reason}")

    # Additional insights
    insights = []

    # Age comparison
    car1_year = car1_data["inputs"]["year"]
    car2_year = car2_data["inputs"]["year"]
    if car1_year != car2_year:
        newer = "Car 1" if car1_year > car2_year else "Car 2"
        insights.append(f"{newer} is newer ({max(car1_year, car2_year)} vs {min(car1_year, car2_year)})")

    # Mileage comparison
    car1_km = car1_data["inputs"]["km"]
    car2_km = car2_data["inputs"]["km"]
    if abs(car1_km - car2_km) > 10000:
        lower = "Car 1" if car1_km < car2_km else "Car 2"
        insights.append(f"{lower} has lower mileage ({min(car1_km, car2_km):,} vs {max(car1_km, car2_km):,} km)")

    # Depreciation comparison
    car1_dep = car1_data["depreciation_data"]["basic_capped"]
    car2_dep = car2_data["depreciation_data"]["basic_capped"]
    if abs(car1_dep - car2_dep) > 0.05:
        lower = "Car 1" if car1_dep < car2_dep else "Car 2"
        insights.append(f"{lower} has less depreciation ({format_percentage(min(car1_dep, car2_dep))} vs {format_percentage(max(car1_dep, car2_dep))})")

    if insights:
        st.markdown("**Key Differences:**")
        for insight in insights:
            st.caption(f"- {insight}")

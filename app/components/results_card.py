"""Results card component for displaying valuation results."""

import streamlit as st
from app.utils.formatters import format_currency_lakhs, format_percentage


def get_verdict_styling(color: str) -> tuple[str, str]:
    """Get background and text color for verdict."""
    styles = {
        "success": ("#00C853", "#FFFFFF"),
        "warning": ("#FFB300", "#000000"),
        "error": ("#FF5252", "#FFFFFF"),
    }
    return styles.get(color, ("#4A9EFF", "#FFFFFF"))


def render_results_card(
    fair_value: float,
    fair_value_min: float,
    fair_value_max: float,
    asking_price: float,
    verdict_data: dict,
    negotiation_target: float,
    fair_value_data: dict = None,
    use_advanced: bool = False,
) -> None:
    """
    Render the main results card.

    Args:
        fair_value: Calculated fair market value
        fair_value_min: Lower bound of fair value range
        fair_value_max: Upper bound of fair value range
        asking_price: Seller's asking price
        verdict_data: Dict with verdict, emoji, color, difference_percent, difference_amount
        negotiation_target: Suggested price to negotiate to
        fair_value_data: Full fair value data with basic and advanced values
        use_advanced: Whether advanced options were used
    """
    st.subheader("Valuation Results")

    # Show comparison if advanced options were used
    if use_advanced and fair_value_data:
        st.caption("Showing both Basic (video formula) and Advanced (with edge cases) values")

        col_basic, col_advanced = st.columns(2)

        with col_basic:
            st.markdown("**Basic Formula**")
            st.metric(
                label="Fair Value (Basic)",
                value=format_currency_lakhs(fair_value_data["basic_adjusted"]),
                help="Standard formula from videos: Life Dep + Owner Premium + Mileage",
            )
            st.caption(
                f"Range: {format_currency_lakhs(fair_value_data['basic_min'])} - "
                f"{format_currency_lakhs(fair_value_data['basic_max'])}"
            )

        with col_advanced:
            st.markdown("**With Edge Cases**")
            adjustment_diff = fair_value_data["adjustment_difference"]
            delta_str = format_currency_lakhs(abs(adjustment_diff))
            if adjustment_diff > 0:
                delta_display = f"-{delta_str}"  # Advanced is lower
            elif adjustment_diff < 0:
                delta_display = f"+{delta_str}"  # Advanced is higher
            else:
                delta_display = None

            st.metric(
                label="Fair Value (Adjusted)",
                value=format_currency_lakhs(fair_value_data["advanced_adjusted"]),
                delta=delta_display,
                delta_color="off",
                help="Includes brand, transmission, condition adjustments",
            )
            st.caption(
                f"Range: {format_currency_lakhs(fair_value_data['advanced_min'])} - "
                f"{format_currency_lakhs(fair_value_data['advanced_max'])}"
            )

        st.info(
            f"**Using Advanced Value** for verdict. "
            f"Edge case adjustments: {format_currency_lakhs(abs(adjustment_diff))} "
            f"{'lower' if adjustment_diff > 0 else 'higher'} than basic."
        )
    else:
        # Standard single value display (basic formula)
        st.metric(
            label="Fair Market Value",
            value=format_currency_lakhs(fair_value),
            help=f"Range: {format_currency_lakhs(fair_value_min)} - {format_currency_lakhs(fair_value_max)}",
        )

        st.caption(
            f"Fair Value Range: {format_currency_lakhs(fair_value_min)} - {format_currency_lakhs(fair_value_max)}"
        )

    st.divider()

    # Verdict display
    verdict = verdict_data["verdict"]
    color = verdict_data["color"]
    diff_percent = verdict_data["difference_percent"]
    diff_amount = verdict_data["difference_amount"]

    bg_color, text_color = get_verdict_styling(color)

    # Verdict badge
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            color: {text_color};
            padding: 12px 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
            margin: 10px 0;
        ">
            {verdict}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Comparison metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Asking Price",
            value=format_currency_lakhs(asking_price),
        )

    with col2:
        delta_color = "inverse" if diff_amount > 0 else "normal"
        st.metric(
            label="Difference",
            value=format_currency_lakhs(abs(diff_amount)),
            delta=format_percentage(diff_percent),
            delta_color=delta_color,
        )

    st.divider()

    # Negotiation suggestion
    if verdict in ["Overpriced", "Slightly Overpriced", "Fair Price"]:
        st.markdown("**Negotiation Target**")
        st.info(
            f"Try negotiating to **{format_currency_lakhs(negotiation_target)}**"
        )

        savings = asking_price - negotiation_target
        if savings > 0:
            st.caption(f"Potential savings: {format_currency_lakhs(savings)}")

    elif verdict in ["Good Deal", "Great Deal"]:
        st.success(
            f"Price is {format_percentage(abs(diff_percent))} below fair value. "
            "Good opportunity if condition checks out!"
        )

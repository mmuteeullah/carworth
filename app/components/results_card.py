"""Results card component for displaying valuation results."""

import streamlit as st
import streamlit_shadcn_ui as ui
from app.utils.formatters import format_currency_lakhs, format_percentage


def get_verdict_variant(color: str) -> str:
    """Get badge variant for verdict."""
    variants = {
        "success": "default",  # Green
        "warning": "secondary",  # Yellow/Orange
        "error": "destructive",  # Red
    }
    return variants.get(color, "outline")


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
    Render the main results card with shadcn components.

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
    # Results header with icon
    st.markdown("### 📊 Valuation Results")

    # Show comparison if advanced options were used
    if use_advanced and fair_value_data:
        st.caption("Comparing Basic (video formula) vs Advanced (with edge cases)")

        col_basic, col_advanced = st.columns(2)

        with col_basic:
            ui.metric_card(
                title="Basic Formula",
                content=format_currency_lakhs(fair_value_data["basic_adjusted"]),
                description=f"Range: {format_currency_lakhs(fair_value_data['basic_min'])} - {format_currency_lakhs(fair_value_data['basic_max'])}",
                key="metric_basic",
            )

        with col_advanced:
            adjustment_diff = fair_value_data["adjustment_difference"]
            delta_text = f"{'↓' if adjustment_diff > 0 else '↑'} {format_currency_lakhs(abs(adjustment_diff))} from basic"

            ui.metric_card(
                title="With Edge Cases",
                content=format_currency_lakhs(fair_value_data["advanced_adjusted"]),
                description=delta_text,
                key="metric_advanced",
            )

        # Info about which is used
        ui.alert_dialog(
            show=False,
            title="Using Advanced Value",
            description=f"Edge case adjustments make value {format_currency_lakhs(abs(adjustment_diff))} {'lower' if adjustment_diff > 0 else 'higher'} than basic.",
            confirm_label="OK",
            key="alert_advanced_info",
        )
        st.info(
            f"**Using Advanced Value** for verdict. "
            f"Adjustments: {format_currency_lakhs(abs(adjustment_diff))} "
            f"{'lower' if adjustment_diff > 0 else 'higher'}"
        )
    else:
        # Standard single value display using metric card
        ui.metric_card(
            title="Fair Market Value",
            content=format_currency_lakhs(fair_value),
            description=f"Range: {format_currency_lakhs(fair_value_min)} - {format_currency_lakhs(fair_value_max)}",
            key="metric_fair_value",
        )

    st.markdown("")  # Spacer

    # Verdict display with badge
    verdict = verdict_data["verdict"]
    color = verdict_data["color"]
    diff_percent = verdict_data["difference_percent"]
    diff_amount = verdict_data["difference_amount"]

    # Verdict badge - centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        badge_variant = get_verdict_variant(color)
        # Use custom styled div for better mobile visibility
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
                padding: 16px 24px;
                border-radius: 12px;
                text-align: center;
                font-size: 1.3rem;
                font-weight: 700;
                margin: 12px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            ">
                {verdict}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")  # Spacer

    # Comparison metrics in cards
    col1, col2 = st.columns(2)

    with col1:
        ui.metric_card(
            title="Asking Price",
            content=format_currency_lakhs(asking_price),
            description="Seller's price",
            key="metric_asking",
        )

    with col2:
        direction = "above" if diff_amount > 0 else "below"
        ui.metric_card(
            title="Difference",
            content=format_currency_lakhs(abs(diff_amount)),
            description=f"{format_percentage(abs(diff_percent))} {direction} fair value",
            key="metric_diff",
        )

    st.markdown("")  # Spacer

    # Negotiation suggestion
    if verdict in ["Overpriced", "Slightly Overpriced", "Fair Price"]:
        st.markdown("#### 🎯 Negotiation Target")

        savings = asking_price - negotiation_target

        ui.metric_card(
            title="Target Price",
            content=format_currency_lakhs(negotiation_target),
            description=f"Potential savings: {format_currency_lakhs(savings)}" if savings > 0 else "Fair starting point",
            key="metric_target",
        )

    elif verdict in ["Good Deal", "Great Deal"]:
        # Success message
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                padding: 16px 20px;
                border-radius: 12px;
                margin: 12px 0;
            ">
                <strong>✓ Good opportunity!</strong><br>
                <span style="font-size: 0.9rem;">
                    Price is {format_percentage(abs(diff_percent))} below fair value.
                    Proceed if condition checks out.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

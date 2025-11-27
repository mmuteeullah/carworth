"""Warnings and alerts component."""

import streamlit as st


def render_warnings(warnings: list[dict]) -> None:
    """
    Render warning messages.

    Args:
        warnings: List of warning dicts with type, title, message
    """
    if not warnings:
        return

    st.subheader("Warnings & Alerts")

    for warning in warnings:
        warning_type = warning["type"]
        title = warning["title"]
        message = warning["message"]

        if warning_type == "danger":
            st.error(f"**{title}**  \n{message}")
        elif warning_type == "warning":
            st.warning(f"**{title}**  \n{message}")
        else:  # info
            st.info(f"**{title}**  \n{message}")


def render_limitations() -> None:
    """Render calculator limitations and disclaimer."""
    st.subheader("Limitations & Disclaimer")

    with st.expander("View Limitations", expanded=False):
        st.markdown("""
        **Calculator Limitations:**

        - **No real-time pricing**: Uses estimated ex-showroom prices
        - **Regional demand**: Doesn't account for city-specific demand variations
        - **Subjective condition**: Condition assessment is self-reported
        - **Market fluctuations**: Doesn't account for seasonal price changes
        - **Special editions**: Limited/special edition models may vary significantly
        - **Modifications**: Aftermarket modifications not accounted for
        - **Rare models**: Discontinued or rare models may command premium
        - **Color impact**: Popular colors may affect resale (not factored)
        """)

    st.caption(
        "**Disclaimer:** CarWorth provides estimated fair values based on standard "
        "depreciation formulas and publicly available data. Actual market prices may "
        "vary based on condition, demand, location, and negotiation. Always conduct "
        "physical inspection and verify service history before purchasing. This "
        "calculator is for informational purposes only and should not be considered "
        "financial advice."
    )

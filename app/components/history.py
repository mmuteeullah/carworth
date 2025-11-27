"""Local history component for storing recent valuations."""

import streamlit as st
from datetime import datetime
from app.utils.formatters import format_currency_lakhs


def init_history():
    """Initialize history in session state."""
    if "valuation_history" not in st.session_state:
        st.session_state["valuation_history"] = []


def add_to_history(inputs: dict, fair_value: float, verdict: str):
    """
    Add a valuation to history.

    Args:
        inputs: User input values
        fair_value: Calculated fair value
        verdict: Verdict string
    """
    init_history()

    # Create history entry
    entry = {
        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "year": inputs["year"],
        "fuel_type": inputs["fuel_type"],
        "ex_showroom": inputs["ex_showroom"],
        "asking_price": inputs["asking_price"],
        "km": inputs["km"],
        "state": inputs["state"],
        "fair_value": fair_value,
        "verdict": verdict,
    }

    # Add to history (most recent first)
    st.session_state["valuation_history"].insert(0, entry)

    # Keep only last 10 entries
    if len(st.session_state["valuation_history"]) > 10:
        st.session_state["valuation_history"] = st.session_state["valuation_history"][:10]


def render_history():
    """Render the history section."""
    init_history()

    history = st.session_state["valuation_history"]

    if not history:
        st.caption("No recent valuations. History will appear here after you calculate a car's value.")
        return

    st.markdown("**Recent Valuations (this session)**")

    for i, entry in enumerate(history):
        # Color based on verdict
        if entry["verdict"] in ["Great Deal", "Good Deal"]:
            color = "green"
        elif entry["verdict"] in ["Overpriced"]:
            color = "red"
        else:
            color = "orange"

        with st.expander(
            f"{entry['year']} {entry['fuel_type']} - {entry['verdict']}",
            expanded=(i == 0),  # Most recent expanded
        ):
            col1, col2 = st.columns(2)

            with col1:
                st.caption(f"Calculated: {entry['timestamp']}")
                st.text(f"Ex-Showroom: {format_currency_lakhs(entry['ex_showroom'])}")
                st.text(f"Kilometers: {entry['km']:,} km")
                st.text(f"State: {entry['state']}")

            with col2:
                st.text(f"Asking Price: {format_currency_lakhs(entry['asking_price'])}")
                st.text(f"Fair Value: {format_currency_lakhs(entry['fair_value'])}")

                # Verdict with color
                if color == "green":
                    st.success(entry["verdict"])
                elif color == "red":
                    st.error(entry["verdict"])
                else:
                    st.warning(entry["verdict"])


def clear_history():
    """Clear all history."""
    st.session_state["valuation_history"] = []

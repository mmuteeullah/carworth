"""Warnings and alerts component with shadcn styling."""

import streamlit as st
import streamlit_shadcn_ui as ui


def render_warnings(warnings: list[dict]) -> None:
    """
    Render warning messages with styled alerts.

    Args:
        warnings: List of warning dicts with type, title, message
    """
    if not warnings:
        return

    st.markdown("### ⚠️ Warnings & Alerts")

    for i, warning in enumerate(warnings):
        warning_type = warning["type"]
        title = warning["title"]
        message = warning["message"]

        # Choose icon and colors based on type
        if warning_type == "danger":
            icon = "🚨"
            bg_color = "rgba(239, 68, 68, 0.1)"
            border_color = "#ef4444"
            text_color = "#fca5a5"
        elif warning_type == "warning":
            icon = "⚠️"
            bg_color = "rgba(245, 158, 11, 0.1)"
            border_color = "#f59e0b"
            text_color = "#fcd34d"
        else:  # info
            icon = "ℹ️"
            bg_color = "rgba(59, 130, 246, 0.1)"
            border_color = "#3b82f6"
            text_color = "#93c5fd"

        # Custom styled alert for better visibility
        st.markdown(
            f"""
            <div style="
                background-color: {bg_color};
                border-left: 4px solid {border_color};
                border-radius: 8px;
                padding: 12px 16px;
                margin: 8px 0;
            ">
                <div style="font-weight: 600; color: {text_color}; margin-bottom: 4px;">
                    {icon} {title}
                </div>
                <div style="font-size: 0.9rem; color: #d1d5db;">
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_limitations() -> None:
    """Render calculator limitations and disclaimer with modern styling."""
    st.markdown("### 📋 Limitations & Disclaimer")

    # Use expander with custom content
    with st.expander("View Limitations", expanded=False):
        limitations = [
            ("📊", "No real-time pricing", "Uses estimated ex-showroom prices"),
            ("📍", "Regional demand", "City-specific demand variations not factored"),
            ("🔍", "Subjective condition", "Condition assessment is self-reported"),
            ("📈", "Market fluctuations", "Seasonal price changes not included"),
            ("⭐", "Special editions", "Limited editions may vary significantly"),
            ("🔧", "Modifications", "Aftermarket mods not accounted for"),
            ("🚗", "Rare models", "Discontinued models may command premium"),
            ("🎨", "Color impact", "Popular colors affect resale (not factored)"),
        ]

        for icon, title, desc in limitations:
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    align-items: flex-start;
                    padding: 8px 0;
                    border-bottom: 1px solid #333;
                ">
                    <span style="font-size: 1.2rem; margin-right: 12px;">{icon}</span>
                    <div>
                        <div style="font-weight: 500; color: #e5e7eb;">{title}</div>
                        <div style="font-size: 0.85rem; color: #9ca3af;">{desc}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Disclaimer in a subtle box
    st.markdown(
        """
        <div style="
            background-color: rgba(75, 85, 99, 0.2);
            border-radius: 8px;
            padding: 12px 16px;
            margin-top: 12px;
            font-size: 0.85rem;
            color: #9ca3af;
        ">
            <strong style="color: #d1d5db;">Disclaimer:</strong>
            CarWorth provides estimated fair values based on standard depreciation formulas.
            Actual market prices may vary. Always conduct physical inspection and verify
            service history before purchasing. For informational purposes only.
        </div>
        """,
        unsafe_allow_html=True,
    )

"""Due diligence checklist component."""

import streamlit as st
from app.calculators.verdict import get_checklist


def render_checklist() -> None:
    """Render the due diligence checklist with modern styling."""
    st.markdown("### ✅ Due Diligence Checklist")

    checklist = get_checklist()

    with st.expander("Before You Buy - Verification Checklist", expanded=False):
        for category in checklist:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #1e3a5f 0%, #172554 100%);
                    border-radius: 8px;
                    padding: 10px 14px;
                    margin: 12px 0 8px 0;
                    font-weight: 600;
                    color: #93c5fd;
                ">
                    {category['category']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            for item in category["items"]:
                st.checkbox(
                    item,
                    key=f"check_{item[:20].replace(' ', '_')}",
                    value=False,
                )

        st.markdown("")  # Spacer

        st.info(
            "💡 **Pro Tip:** Consider getting a professional "
            "pre-purchase inspection for peace of mind."
        )

"""Due diligence checklist component."""

import streamlit as st
from app.calculators.verdict import get_checklist


def render_checklist() -> None:
    """Render the due diligence checklist."""
    st.subheader("Due Diligence Checklist")

    checklist = get_checklist()

    with st.expander("Before You Buy - Verification Checklist", expanded=False):
        for category in checklist:
            st.markdown(f"**{category['category']}**")

            for item in category["items"]:
                st.checkbox(
                    item,
                    key=f"check_{item[:20]}",
                    value=False,
                )

            st.markdown("")  # Spacing

        st.info(
            "This checklist is for guidance only. Consider getting a professional "
            "pre-purchase inspection for peace of mind."
        )

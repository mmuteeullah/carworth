"""CarWorth - Used Car Value Calculator main entry point."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.config import APP_TITLE, APP_DESCRIPTION, PAGE_LAYOUT
from app.components.input_form import render_input_form
from app.components.results_card import render_results_card
from app.components.breakdown import render_breakdown
from app.components.warnings import render_warnings, render_limitations
from app.components.checklist import render_checklist
from app.calculators.on_road_price import calculate_on_road_price
from app.calculators.depreciation import calculate_total_depreciation
from app.calculators.fair_value import calculate_complete_fair_value
from app.calculators.verdict import get_verdict, get_negotiation_target, generate_warnings
from app.utils.validators import validate_inputs


def load_css():
    """Load custom CSS styles."""
    # Add viewport meta tag for mobile
    st.markdown(
        """
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        """,
        unsafe_allow_html=True,
    )

    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_header():
    """Render the app header with logo."""
    col1, col2 = st.columns([1, 5])

    logo_path = Path(__file__).parent / "assets" / "logo.png"
    with col1:
        if logo_path.exists():
            st.image(str(logo_path), width=80)

    with col2:
        st.title(APP_TITLE)
        st.caption(APP_DESCRIPTION)


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="car",
        layout=PAGE_LAYOUT,
        initial_sidebar_state="collapsed",
    )

    # Load custom styles
    load_css()

    # Header
    render_header()

    st.divider()

    # Input form (single column for mobile-friendly layout)
    inputs = render_input_form()

    calculate_clicked = st.button(
        "Calculate Fair Value",
        type="primary",
        use_container_width=True,
    )

    st.divider()

    # Results section
    if calculate_clicked:
        # Validate inputs
        is_valid, errors = validate_inputs(inputs)

        if not is_valid:
            for error in errors:
                st.error(error)
        else:
            # Run calculations
            with st.spinner("Calculating..."):
                # Step 1: On-road price
                on_road_data = calculate_on_road_price(
                    ex_showroom=inputs["ex_showroom"],
                    state=inputs["state"],
                    fuel_type=inputs["fuel_type"],
                )

                # Step 2: Depreciation
                depreciation_data = calculate_total_depreciation(
                    year=inputs["year"],
                    fuel_type=inputs["fuel_type"],
                    state=inputs["state"],
                    owner=inputs["owner"],
                    km=inputs["km"],
                    brand=inputs["brand"],
                    transmission=inputs["transmission"],
                    body_condition=inputs["body_condition"],
                    accident_history=inputs["accident_history"],
                    service_history=inputs["service_history"],
                    commercial_use=inputs["commercial_use"],
                    new_gen_available=inputs["new_gen_available"],
                )

                # Step 3: Fair value
                insurance_valid = inputs["insurance_status"] == "Valid"
                fair_value_data = calculate_complete_fair_value(
                    on_road_price=on_road_data["on_road_price"],
                    total_depreciation=depreciation_data["total_capped"],
                    insurance_valid=insurance_valid,
                    ex_showroom=inputs["ex_showroom"],
                )

                # Step 4: Verdict
                verdict_data = get_verdict(
                    asking_price=inputs["asking_price"],
                    fair_value=fair_value_data["fair_value"],
                )

                negotiation_target = get_negotiation_target(
                    fair_value=fair_value_data["fair_value"],
                    verdict_result=verdict_data,
                )

                # Step 5: Warnings
                warnings = generate_warnings(
                    fuel_type=inputs["fuel_type"],
                    state=inputs["state"],
                    age=depreciation_data["age"],
                    mileage_status=depreciation_data["mileage_status"],
                    owner=inputs["owner"],
                    accident_history=inputs["accident_history"],
                    commercial_use=inputs["commercial_use"],
                    transmission=inputs["transmission"],
                )

            # Display results
            render_results_card(
                fair_value=fair_value_data["fair_value"],
                fair_value_min=fair_value_data["fair_value_min"],
                fair_value_max=fair_value_data["fair_value_max"],
                asking_price=inputs["asking_price"],
                verdict_data=verdict_data,
                negotiation_target=negotiation_target,
            )

            # Store in session for breakdown
            st.session_state["on_road_data"] = on_road_data
            st.session_state["depreciation_data"] = depreciation_data
            st.session_state["fair_value_data"] = fair_value_data
            st.session_state["warnings"] = warnings
            st.session_state["calculated"] = True

    else:
        st.info("Enter car details and click **Calculate Fair Value** to see results.")

    # Below the main columns - additional sections
    if st.session_state.get("calculated"):
        st.divider()

        # Warnings section
        if st.session_state.get("warnings"):
            render_warnings(st.session_state["warnings"])
            st.divider()

        # Breakdown section
        render_breakdown(
            on_road_data=st.session_state["on_road_data"],
            depreciation_data=st.session_state["depreciation_data"],
            fair_value_data=st.session_state["fair_value_data"],
        )

        st.divider()

        # Checklist
        render_checklist()

        st.divider()

    # Always show limitations
    render_limitations()

    # Footer
    st.divider()
    st.caption(
        "CarWorth v1.0 | "
        "For informational purposes only | "
        "Always verify before purchase"
    )


if __name__ == "__main__":
    main()

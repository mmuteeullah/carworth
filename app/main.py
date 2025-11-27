"""CarWorth - Used Car Value Calculator main entry point."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import streamlit_shadcn_ui as ui

from app.config import APP_TITLE, APP_DESCRIPTION, PAGE_LAYOUT
from app.components.input_form import render_input_form, render_comparison_form
from app.components.results_card import render_results_card
from app.components.breakdown import render_breakdown
from app.components.warnings import render_warnings, render_limitations
from app.components.checklist import render_checklist
from app.components.comparison_results import render_comparison_results
from app.components.history import init_history, add_to_history, render_history
from app.calculators.on_road_price import calculate_on_road_price
from app.calculators.depreciation import calculate_total_depreciation
from app.calculators.fair_value import calculate_complete_fair_value
from app.calculators.verdict import get_verdict, get_negotiation_target, generate_warnings
from app.utils.validators import validate_inputs
from app.utils.pdf_generator import generate_valuation_report


def calculate_car_value(inputs: dict) -> dict:
    """
    Run all calculations for a single car.

    Returns dict with all calculation results.
    """
    on_road_data = calculate_on_road_price(
        ex_showroom=inputs["ex_showroom"],
        state=inputs["state"],
        fuel_type=inputs["fuel_type"],
        custom_road_tax_rate=inputs.get("custom_road_tax_rate"),
    )

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

    insurance_valid = inputs["insurance_status"] == "Valid"
    use_advanced = inputs["use_advanced"]
    fair_value_data = calculate_complete_fair_value(
        on_road_price=on_road_data["on_road_price"],
        basic_depreciation=depreciation_data["basic_capped"],
        advanced_depreciation=depreciation_data["advanced_capped"],
        insurance_valid=insurance_valid,
        ex_showroom=inputs["ex_showroom"],
        use_advanced=use_advanced,
    )

    verdict_data = get_verdict(
        asking_price=inputs["asking_price"],
        fair_value=fair_value_data["fair_value"],
    )

    negotiation_target = get_negotiation_target(
        fair_value=fair_value_data["fair_value"],
        verdict_result=verdict_data,
    )

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

    return {
        "inputs": inputs,
        "on_road_data": on_road_data,
        "depreciation_data": depreciation_data,
        "fair_value_data": fair_value_data,
        "verdict_data": verdict_data,
        "negotiation_target": negotiation_target,
        "warnings": warnings,
        "use_advanced": use_advanced,
    }


def load_css():
    """Load custom CSS styles and security meta tags."""
    # Add viewport and security meta tags
    st.markdown(
        """
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="referrer" content="strict-origin-when-cross-origin">
        <meta http-equiv="X-Content-Type-Options" content="nosniff">
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

    # Initialize history
    init_history()

    # Load custom styles
    load_css()

    # Header
    render_header()

    st.divider()

    # Mode toggle using shadcn tabs
    mode = ui.tabs(
        options=["Single Car", "Compare Two Cars"],
        default_value="Single Car",
        key="mode_selector",
    )

    comparison_mode = mode == "Compare Two Cars"

    st.markdown("")  # Spacer

    if comparison_mode:
        # Comparison mode
        car1_inputs, car2_inputs = render_comparison_form()

        calculate_clicked = st.button(
            "Compare Cars",
            type="primary",
            use_container_width=True,
        )

        st.divider()

        if calculate_clicked:
            # Validate both cars
            car1_valid, car1_errors = validate_inputs(car1_inputs)
            car2_valid, car2_errors = validate_inputs(car2_inputs)

            if not car1_valid or not car2_valid:
                if car1_errors:
                    st.error(f"**Car 1:** {', '.join(car1_errors)}")
                if car2_errors:
                    st.error(f"**Car 2:** {', '.join(car2_errors)}")
            else:
                with st.spinner("Calculating..."):
                    car1_data = calculate_car_value(car1_inputs)
                    car2_data = calculate_car_value(car2_inputs)

                render_comparison_results(car1_data, car2_data)

                # Store in session
                st.session_state["comparison_mode"] = True
                st.session_state["car1_data"] = car1_data
                st.session_state["car2_data"] = car2_data
                st.session_state["calculated"] = True

        else:
            st.info("Enter details for both cars and click **Compare Cars** to see results.")

    else:
        # Single car mode
        inputs = render_input_form()

        calculate_clicked = st.button(
            "Calculate Fair Value",
            type="primary",
            use_container_width=True,
        )

        st.divider()

        if calculate_clicked:
            is_valid, errors = validate_inputs(inputs)

            if not is_valid:
                for error in errors:
                    st.error(error)
            else:
                with st.spinner("Calculating..."):
                    result = calculate_car_value(inputs)

                # Display results
                render_results_card(
                    fair_value=result["fair_value_data"]["fair_value"],
                    fair_value_min=result["fair_value_data"]["fair_value_min"],
                    fair_value_max=result["fair_value_data"]["fair_value_max"],
                    asking_price=inputs["asking_price"],
                    verdict_data=result["verdict_data"],
                    negotiation_target=result["negotiation_target"],
                    fair_value_data=result["fair_value_data"],
                    use_advanced=result["use_advanced"],
                )

                # Store in session for breakdown
                st.session_state["on_road_data"] = result["on_road_data"]
                st.session_state["depreciation_data"] = result["depreciation_data"]
                st.session_state["fair_value_data"] = result["fair_value_data"]
                st.session_state["warnings"] = result["warnings"]
                st.session_state["calculated"] = True
                st.session_state["comparison_mode"] = False
                st.session_state["use_advanced"] = result["use_advanced"]
                st.session_state["inputs"] = inputs
                st.session_state["verdict_data"] = result["verdict_data"]
                st.session_state["negotiation_target"] = result["negotiation_target"]

                # Add to history
                add_to_history(
                    inputs=inputs,
                    fair_value=result["fair_value_data"]["fair_value"],
                    verdict=result["verdict_data"]["verdict"],
                )

        else:
            st.info("Enter car details and click **Calculate Fair Value** to see results.")

    # Below the main columns - additional sections (single car mode only)
    if st.session_state.get("calculated") and not st.session_state.get("comparison_mode"):
        st.divider()

        # Warnings section
        if st.session_state.get("warnings"):
            render_warnings(st.session_state["warnings"])
            st.divider()

        # PDF Download button
        pdf_bytes = generate_valuation_report(
            inputs=st.session_state["inputs"],
            on_road_data=st.session_state["on_road_data"],
            depreciation_data=st.session_state["depreciation_data"],
            fair_value_data=st.session_state["fair_value_data"],
            verdict_data=st.session_state["verdict_data"],
            negotiation_target=st.session_state["negotiation_target"],
            warnings=st.session_state.get("warnings", []),
        )
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"carworth_report_{st.session_state['inputs']['year']}_{st.session_state['inputs']['fuel_type'].lower()}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

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

    # History section
    with st.expander("Recent Valuations", expanded=False):
        render_history()

    st.divider()

    # Always show limitations
    render_limitations()

    # Footer
    st.divider()
    st.caption(
        "CarWorth v2.0 | "
        "For informational purposes only | "
        "Always verify before purchase"
    )


if __name__ == "__main__":
    main()

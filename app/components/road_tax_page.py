"""Road Tax Reference page component."""

import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from app.data.road_tax import (
    STATE_TAX_CONFIG,
    get_state_tax_table,
    get_all_states_summary,
    get_all_states,
)
from app.data.gst import (
    get_gst_rates_table,
    get_gst_impact_summary,
    SMALL_CAR_THRESHOLDS,
)


def render_road_tax_page() -> None:
    """Render the Road Tax Reference page."""

    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 24px;">
            <h1 style="color: #f3f4f6; margin-bottom: 8px;">🚗 Tax Reference</h1>
            <p style="color: #9ca3af; font-size: 1rem;">
                Road Tax & GST rates for cars in India (2024-25)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tab selection
    tax_tab = ui.tabs(
        options=["Road Tax by State", "GST Rates"],
        default_value="Road Tax by State",
        key="tax_reference_tabs",
    )

    st.markdown("")  # Spacer

    if tax_tab == "GST Rates":
        render_gst_section()
        return

    # Road Tax section (original content)
    # Summary table
    st.markdown("### 📊 All States Summary")
    st.markdown(
        """
        <div style="
            background-color: rgba(59, 130, 246, 0.1);
            border-left: 3px solid #3b82f6;
            padding: 10px 12px;
            margin-bottom: 16px;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #93c5fd;
        ">
            Click on any state below to see detailed slab-wise breakdown
        </div>
        """,
        unsafe_allow_html=True,
    )

    summary = get_all_states_summary()

    # Create DataFrame for display
    df_summary = pd.DataFrame(summary)
    df_summary.columns = ["State", "Petrol", "Diesel", "Electric", "Slabs"]

    # Style the dataframe
    st.dataframe(
        df_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "State": st.column_config.TextColumn("State", width="medium"),
            "Petrol": st.column_config.TextColumn("Petrol", width="small"),
            "Diesel": st.column_config.TextColumn("Diesel", width="small"),
            "Electric": st.column_config.TextColumn("EV", width="small"),
            "Slabs": st.column_config.NumberColumn("# Slabs", width="small"),
        },
    )

    st.markdown("---")

    # State selector for detailed view
    st.markdown("### 🔍 Detailed State View")

    all_states = get_all_states()

    selected_state = st.selectbox(
        "Select State",
        options=all_states,
        index=all_states.index("Maharashtra") if "Maharashtra" in all_states else 0,
        key="road_tax_state_selector",
    )

    if selected_state:
        render_state_details(selected_state)

    # Footer notes
    st.markdown("---")
    st.markdown(
        """
        <div style="
            background-color: rgba(245, 158, 11, 0.1);
            border-left: 3px solid #f59e0b;
            padding: 12px 16px;
            border-radius: 4px;
            margin-top: 16px;
        ">
            <div style="color: #fcd34d; font-weight: 600; margin-bottom: 8px;">
                ⚠️ Important Notes
            </div>
            <ul style="color: #fde68a; font-size: 0.85rem; margin: 0; padding-left: 20px;">
                <li>Rates are based on 2024-25 data from official RTO sources</li>
                <li>Company/commercial registration typically has higher rates (often 2x)</li>
                <li>Some states charge additional infrastructure cess or green tax</li>
                <li>Always verify with your local RTO for the most current rates</li>
                <li>EV incentives may vary and are subject to policy changes</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Data sources
    st.markdown("#### 📚 Data Sources")
    st.markdown(
        """
        - [Cars24 - RTO Charges](https://www.cars24.com/article/car-registration-charges-in-india-rto-charges-for-new-car-road-tax-slabs/)
        - [CreditMantri - Road Tax Rates](https://www.creditmantri.com/road-taxes-in-states-and-uts-of-india/)
        - State RTO Official Websites
        """
    )


def render_state_details(state: str) -> None:
    """Render detailed tax table for a specific state."""

    config = STATE_TAX_CONFIG.get(state)
    if not config:
        st.error(f"State '{state}' not found")
        return

    slabs = config["slabs"]
    rates = config["rates"]

    # State header
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1e3a5f 0%, #172554 100%);
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
        ">
            <h3 style="color: #f3f4f6; margin: 0 0 8px 0;">{state}</h3>
            <p style="color: #93c5fd; margin: 0; font-size: 0.9rem;">
                {len(slabs)} price slab{'s' if len(slabs) > 1 else ''} •
                Petrol: {_get_rate_range(rates['Petrol'])} •
                Diesel: {_get_rate_range(rates['Diesel'])}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Build table data
    slab_names = [s[1] for s in slabs]
    slab_ranges = [s[2] for s in slabs]

    # Create data for each fuel type
    table_data = []
    for fuel_type in ["Petrol", "Diesel", "CNG", "Hybrid", "Electric"]:
        fuel_rates = rates.get(fuel_type, {})
        row = {"Fuel Type": fuel_type}
        for i, slab_name in enumerate(slab_names):
            rate = fuel_rates.get(slab_name, 0)
            row[slab_ranges[i]] = f"{rate * 100:.1f}%"
        table_data.append(row)

    df = pd.DataFrame(table_data)

    # Display table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    # Slab boundaries explanation
    st.markdown("#### 📏 Price Slab Boundaries")

    for upper_limit, slab_name, slab_range in slabs:
        if upper_limit == float("inf"):
            boundary_text = "No upper limit"
        else:
            boundary_text = f"Up to ₹{upper_limit/100000:.1f} Lakh"

        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: space-between;
                padding: 8px 12px;
                background-color: #1f2937;
                border-radius: 4px;
                margin-bottom: 4px;
            ">
                <span style="color: #d1d5db;">{slab_range}</span>
                <span style="color: #9ca3af;">{boundary_text}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Special notes for specific states
    _render_state_notes(state)


def _get_rate_range(rates: dict) -> str:
    """Get min-max rate range as string."""
    values = list(rates.values())
    min_rate = min(values) * 100
    max_rate = max(values) * 100
    if min_rate == max_rate:
        return f"{min_rate:.1f}%"
    return f"{min_rate:.1f}% - {max_rate:.1f}%"


def _render_state_notes(state: str) -> None:
    """Render special notes for specific states."""

    notes = {
        "Delhi": [
            "Electric vehicles are completely exempt from road tax",
            "Additional MCD parking fee: ₹2,000 (under ₹4L) or ₹4,000 (above ₹4L)",
            "Diesel vehicles have a 10-year lifespan restriction in NCR",
        ],
        "Karnataka": [
            "Has the highest road tax rates in India",
            "Additional Infrastructure Cess of 11% on road tax applies",
            "EV exemption available until policy review",
        ],
        "Maharashtra": [
            "Company registration is charged at double the rate (20%+)",
            "CNG vehicles get reduced rates compared to petrol",
            "Mumbai and other cities may have additional local charges",
        ],
        "Haryana": [
            "CNG vehicles get 20% rebate on petrol rates",
            "Electric vehicles charged nominal 2% rate",
            "Part of NCR - diesel vehicles have 10-year restriction",
        ],
        "Gujarat": [
            "Has a flat rate structure - same rate regardless of price",
            "Company vehicles taxed at 12% + 5% VAT",
            "One of the lowest tax states for premium vehicles",
        ],
        "Himachal Pradesh": [
            "Lowest road tax rates in India",
            "Rates are actually based on engine capacity, simplified here to price slabs",
            "Popular for vehicle registration due to low taxes",
        ],
        "Tamil Nadu": [
            "Simple two-slab structure",
            "Same rates for petrol and diesel",
            "EV exemption to promote electric adoption",
        ],
        "Telangana": [
            "EV exemption policy effective from November 2024",
            "Rates similar to Andhra Pradesh",
            "Two-slab simple structure",
        ],
        "Punjab": [
            "Includes 1% Social Security Contribution in rates",
            "Actual base rate is 8% + 1% SSC = 9%",
        ],
        "Uttar Pradesh": [
            "Part of NCR - diesel vehicles have 10-year restriction in some areas",
            "Additional temporary charges in metro cities (Noida, Ghaziabad): ₹1,500",
        ],
    }

    state_notes = notes.get(state, [])

    if state_notes:
        st.markdown("#### 📝 Special Notes")
        st.markdown(
            f"""
            <div style="
                background-color: rgba(99, 102, 241, 0.1);
                border-radius: 8px;
                padding: 12px 16px;
            ">
                <ul style="color: #c7d2fe; font-size: 0.85rem; margin: 0; padding-left: 20px;">
                    {''.join(f'<li style="margin-bottom: 4px;">{note}</li>' for note in state_notes)}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_gst_section() -> None:
    """Render GST rates section."""

    st.markdown("### 🧾 GST Rates on Cars (September 2025)")

    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #7c2d12 0%, #431407 100%);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 20px;
        ">
            <h4 style="color: #fed7aa; margin: 0 0 8px 0;">GST Reform 2.0 (Effective Sept 22, 2025)</h4>
            <p style="color: #fde68a; margin: 0; font-size: 0.9rem;">
                Compensation cess abolished! Cars now attract simplified 18% or 40% GST based on size.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # GST rates table
    st.markdown("#### 📊 GST Rate Structure")

    gst_rates = get_gst_rates_table()
    df_gst = pd.DataFrame(gst_rates)
    df_gst.columns = ["Category", "Criteria", "New Rate", "Old Rate"]

    st.dataframe(
        df_gst,
        use_container_width=True,
        hide_index=True,
    )

    # Small car thresholds
    st.markdown("---")
    st.markdown("#### 📏 Small Car Classification Thresholds")

    st.markdown(
        """
        <div style="
            background-color: rgba(59, 130, 246, 0.1);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
        ">
            <p style="color: #93c5fd; margin: 0 0 12px 0; font-size: 0.9rem;">
                A car must meet <strong>BOTH</strong> criteria to qualify for the 18% small car rate:
            </p>
        """,
        unsafe_allow_html=True,
    )

    threshold_data = [
        {"Fuel Type": "Petrol / CNG / LPG", "Max Engine": "≤ 1200 CC", "Max Length": "≤ 4000 mm"},
        {"Fuel Type": "Diesel", "Max Engine": "≤ 1500 CC", "Max Length": "≤ 4000 mm"},
        {"Fuel Type": "Hybrid (Petrol)", "Max Engine": "≤ 1200 CC", "Max Length": "≤ 4000 mm"},
        {"Fuel Type": "Hybrid (Diesel)", "Max Engine": "≤ 1500 CC", "Max Length": "≤ 4000 mm"},
        {"Fuel Type": "Electric", "Max Engine": "N/A", "Max Length": "Any (always 5%)"},
    ]

    df_thresholds = pd.DataFrame(threshold_data)
    st.dataframe(df_thresholds, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Price impact
    st.markdown("---")
    st.markdown("#### 💰 Impact on Car Prices")

    impact_data = get_gst_impact_summary()
    df_impact = pd.DataFrame(impact_data)
    df_impact.columns = ["Car Type", "Old Rate", "New Rate", "Impact"]

    st.dataframe(df_impact, use_container_width=True, hide_index=True)

    # Examples
    st.markdown("---")
    st.markdown("#### 📝 Classification Examples")

    examples = [
        {
            "car": "Maruti Alto K10 (Petrol)",
            "engine": "998 CC",
            "length": "3530 mm",
            "gst": "18%",
            "reason": "✅ Petrol ≤1200cc AND ≤4000mm",
        },
        {
            "car": "Hyundai i20 (Petrol)",
            "engine": "1197 CC",
            "length": "3995 mm",
            "gst": "18%",
            "reason": "✅ Just within limits (1197 ≤ 1200)",
        },
        {
            "car": "Honda City (Petrol)",
            "engine": "1498 CC",
            "length": "4549 mm",
            "gst": "40%",
            "reason": "❌ Exceeds both engine (>1200) and length (>4000)",
        },
        {
            "car": "Hyundai Creta (Petrol)",
            "engine": "1497 CC",
            "length": "4300 mm",
            "gst": "40%",
            "reason": "❌ Engine 1497 > 1200cc limit",
        },
        {
            "car": "Tata Nexon EV",
            "engine": "Electric",
            "length": "3993 mm",
            "gst": "5%",
            "reason": "⚡ All EVs get 5% regardless of size",
        },
    ]

    for ex in examples:
        st.markdown(
            f"""
            <div style="
                background-color: #1f2937;
                border-radius: 6px;
                padding: 12px 16px;
                margin-bottom: 8px;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #f3f4f6; font-weight: 600;">{ex['car']}</span>
                        <span style="color: #9ca3af; font-size: 0.85rem; margin-left: 12px;">
                            {ex['engine']} | {ex['length']}
                        </span>
                    </div>
                    <span style="
                        background-color: {'#166534' if ex['gst'] in ['18%', '5%'] else '#991b1b'};
                        color: white;
                        padding: 4px 12px;
                        border-radius: 4px;
                        font-weight: 600;
                    ">{ex['gst']}</span>
                </div>
                <div style="color: #9ca3af; font-size: 0.8rem; margin-top: 6px;">
                    {ex['reason']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Notes
    st.markdown("---")
    st.markdown(
        """
        <div style="
            background-color: rgba(245, 158, 11, 0.1);
            border-left: 3px solid #f59e0b;
            padding: 12px 16px;
            border-radius: 4px;
        ">
            <div style="color: #fcd34d; font-weight: 600; margin-bottom: 8px;">
                ⚠️ Important Notes
            </div>
            <ul style="color: #fde68a; font-size: 0.85rem; margin: 0; padding-left: 20px;">
                <li>GST is already included in the Ex-Showroom price quoted by dealers</li>
                <li>Used cars: GST applies only on dealer's profit margin, not full sale price</li>
                <li>Imported cars: Subject to additional customs duty + IGST</li>
                <li>Vehicles for disabled persons may receive GST exemptions</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Data sources
    st.markdown("#### 📚 Data Sources")
    st.markdown(
        """
        - [ClearTax - GST on Cars](https://cleartax.in/s/gst-on-cars)
        - [Bajaj Finserv - GST on Cars](https://www.bajajfinserv.in/gst-on-cars)
        - [RazorPay - GST on Cars](https://razorpay.com/learn/gst-on-cars/)
        """
    )

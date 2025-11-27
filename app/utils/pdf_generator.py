"""PDF report generator for CarWorth valuation reports."""

from io import BytesIO
from datetime import datetime
from fpdf import FPDF

from app.utils.formatters import (
    format_currency_lakhs,
    format_percentage,
    format_km,
    format_currency,
)


class CarWorthPDF(FPDF):
    """Custom PDF class for CarWorth reports."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        """Add header to each page."""
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "CarWorth - Valuation Report", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f"Generated on {datetime.now().strftime('%d %b %Y, %I:%M %p')}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def footer(self):
        """Add footer to each page."""
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "For informational purposes only. Always verify before purchase.", align="C")

    def section_title(self, title: str):
        """Add a section title."""
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def add_row(self, label: str, value: str, bold_value: bool = False):
        """Add a label-value row."""
        self.set_font("Helvetica", "", 10)
        self.cell(100, 6, label)
        self.set_font("Helvetica", "B" if bold_value else "", 10)
        self.cell(0, 6, value, new_x="LMARGIN", new_y="NEXT")

    def add_divider(self):
        """Add a horizontal divider line."""
        self.ln(2)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)


def generate_valuation_report(
    inputs: dict,
    on_road_data: dict,
    depreciation_data: dict,
    fair_value_data: dict,
    verdict_data: dict,
    negotiation_target: float,
    warnings: list,
) -> bytes:
    """
    Generate a PDF valuation report.

    Args:
        inputs: User input values
        on_road_data: On-road price calculation data
        depreciation_data: Depreciation calculation data
        fair_value_data: Fair value calculation data
        verdict_data: Verdict determination data
        negotiation_target: Suggested negotiation price
        warnings: List of warning messages

    Returns:
        PDF file as bytes
    """
    pdf = CarWorthPDF()
    pdf.add_page()

    use_advanced = fair_value_data.get("using_advanced", False)

    # Car Details Section
    pdf.section_title("Car Details")
    pdf.add_row("Ex-Showroom Price", format_currency_lakhs(inputs["ex_showroom"]))
    pdf.add_row("Year of Manufacture", str(inputs["year"]))
    pdf.add_row("Fuel Type", inputs["fuel_type"])
    pdf.add_row("Registration State", inputs["state"])
    pdf.add_row("Owner Number", inputs["owner"])
    pdf.add_row("Kilometers Driven", format_km(inputs["km"]))
    pdf.add_row("Insurance Status", inputs["insurance_status"])
    pdf.add_row("Asking Price", format_currency_lakhs(inputs["asking_price"]))

    if use_advanced:
        pdf.ln(2)
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 5, "Advanced options used:", new_x="LMARGIN", new_y="NEXT")
        if inputs.get("brand") and inputs["brand"] != "Other":
            pdf.add_row("  Brand", inputs["brand"])
        if inputs.get("transmission") and inputs["transmission"] != "Manual":
            pdf.add_row("  Transmission", inputs["transmission"])
        if inputs.get("body_condition") and inputs["body_condition"] != "Good":
            pdf.add_row("  Body Condition", inputs["body_condition"])
        if inputs.get("accident_history") and inputs["accident_history"] != "None":
            pdf.add_row("  Accident History", inputs["accident_history"])
        if inputs.get("service_history") and inputs["service_history"] != "Unknown":
            pdf.add_row("  Service History", inputs["service_history"])
        if inputs.get("commercial_use"):
            pdf.add_row("  Commercial Use", "Yes")
        if inputs.get("new_gen_available"):
            pdf.add_row("  New Gen Available", "Yes")

    pdf.ln(5)

    # On-Road Price Section
    pdf.section_title("Step 1: On-Road Price Calculation")
    road_tax_rate = on_road_data["road_tax_rate"]
    is_custom_rate = on_road_data.get("is_custom_rate", False)

    pdf.add_row("Ex-Showroom Price", format_currency_lakhs(on_road_data["ex_showroom"]))
    rate_label = f"Road Tax ({format_percentage(road_tax_rate)})"
    if is_custom_rate:
        rate_label += " [Custom]"
    pdf.add_row(rate_label, format_currency_lakhs(on_road_data["road_tax"]))
    pdf.add_row("Insurance (Estimated)", format_currency_lakhs(on_road_data["insurance"]))
    pdf.add_row("Fixed Charges (Reg + HSRP + FasTag)", format_currency_lakhs(on_road_data["fixed_charges"]))
    pdf.add_divider()
    pdf.add_row("Total On-Road Price", format_currency_lakhs(on_road_data["on_road_price"]), bold_value=True)
    pdf.ln(3)

    # Depreciation Section
    pdf.section_title("Step 2: Depreciation Calculation")
    age = depreciation_data["age"]
    life_years = depreciation_data.get("life_years", 15)

    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 5, f"Basic Formula: Life Dep (Age/{life_years}) + Ownership Premium + Mileage Adjustment", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.add_row(f"Life Depreciation ({age} yrs / {life_years} yrs)", format_percentage(depreciation_data["life_depreciation"]))
    pdf.add_row("Ownership Premium", format_percentage(depreciation_data["ownership_premium"]))
    pdf.add_row("Mileage Adjustment", format_percentage(depreciation_data["mileage_adjustment"]))
    pdf.add_divider()

    basic_label = "Basic Total"
    if depreciation_data.get("basic_is_capped"):
        basic_label += " (Capped at 85%)"
    pdf.add_row(basic_label, format_percentage(depreciation_data["basic_capped"]), bold_value=True)

    if use_advanced:
        pdf.ln(3)
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 5, "Edge Case Adjustments:", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        if depreciation_data["brand_adjustment"] != 0:
            brand_mult = depreciation_data["brand_multiplier"]
            pdf.add_row(f"Brand Adjustment (x{brand_mult:.2f})", format_percentage(depreciation_data["brand_adjustment"]))
        if depreciation_data["transmission_adjustment"] != 0:
            pdf.add_row("Transmission Risk", format_percentage(depreciation_data["transmission_adjustment"]))

        cond = depreciation_data["condition_adjustments"]
        if cond["body"] != 0:
            pdf.add_row("Body Condition", format_percentage(cond["body"]))
        if cond["accident"] != 0:
            pdf.add_row("Accident History", format_percentage(cond["accident"]))
        if cond["service"] != 0:
            pdf.add_row("Service History", format_percentage(cond["service"]))
        if cond["commercial"] != 0:
            pdf.add_row("Commercial Use", format_percentage(cond["commercial"]))
        if cond["new_gen"] != 0:
            pdf.add_row("New Gen Available", format_percentage(cond["new_gen"]))

        pdf.add_divider()
        adv_label = "Advanced Total"
        if depreciation_data.get("advanced_is_capped"):
            adv_label += " (Capped at 85%)"
        pdf.add_row(adv_label, format_percentage(depreciation_data["advanced_capped"]), bold_value=True)

    pdf.ln(5)

    # Fair Value Section
    pdf.section_title("Step 3: Fair Value Calculation")

    if use_advanced:
        pdf.add_row("Basic Fair Value", format_currency_lakhs(fair_value_data["basic_adjusted"]))
        pdf.add_row("Advanced Fair Value", format_currency_lakhs(fair_value_data["advanced_adjusted"]))
        adjustment_diff = fair_value_data["adjustment_difference"]
        diff_text = f"{format_currency_lakhs(abs(adjustment_diff))} {'lower' if adjustment_diff > 0 else 'higher'}"
        pdf.add_row("Edge Case Impact", diff_text)
        pdf.ln(2)
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 5, "Using Advanced Value for verdict", new_x="LMARGIN", new_y="NEXT")
    else:
        on_road = on_road_data["on_road_price"]
        dep_rate = depreciation_data["basic_capped"]
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 5, f"Fair Value = On-Road Price x (1 - Depreciation)", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 5, f"Fair Value = {format_currency_lakhs(on_road)} x (1 - {format_percentage(dep_rate)})", new_x="LMARGIN", new_y="NEXT")

    pdf.add_divider()

    pdf.add_row("Base Fair Value", format_currency_lakhs(fair_value_data["base_fair_value"]))
    if fair_value_data["insurance_deduction"] > 0:
        pdf.add_row("Insurance Deduction (Expired)", f"- {format_currency_lakhs(fair_value_data['insurance_deduction'])}")
    pdf.add_row("Final Fair Value", format_currency_lakhs(fair_value_data["fair_value"]), bold_value=True)
    pdf.add_row("Fair Value Range", f"{format_currency_lakhs(fair_value_data['fair_value_min'])} - {format_currency_lakhs(fair_value_data['fair_value_max'])}")

    pdf.ln(5)

    # Verdict Section
    pdf.section_title("Verdict")
    verdict = verdict_data["verdict"]
    diff_percent = verdict_data["difference_percent"]
    diff_amount = verdict_data["difference_amount"]

    # Color the verdict based on result
    color = verdict_data["color"]
    if color == "success":
        pdf.set_text_color(0, 128, 0)
    elif color == "warning":
        pdf.set_text_color(200, 150, 0)
    elif color == "error":
        pdf.set_text_color(200, 0, 0)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, verdict, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)

    pdf.add_row("Asking Price", format_currency_lakhs(inputs["asking_price"]))
    pdf.add_row("Fair Value", format_currency_lakhs(fair_value_data["fair_value"]))
    pdf.add_row("Difference", f"{format_currency_lakhs(abs(diff_amount))} ({format_percentage(abs(diff_percent))})")

    if verdict in ["Overpriced", "Slightly Overpriced", "Fair Price"]:
        pdf.ln(3)
        pdf.add_row("Negotiation Target", format_currency_lakhs(negotiation_target), bold_value=True)
        savings = inputs["asking_price"] - negotiation_target
        if savings > 0:
            pdf.add_row("Potential Savings", format_currency_lakhs(savings))

    elif verdict in ["Good Deal", "Great Deal"]:
        pdf.ln(3)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 6, f"Price is {format_percentage(abs(diff_percent))} below fair value!", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)

    # Warnings Section (if any)
    if warnings:
        pdf.ln(5)
        pdf.section_title("Warnings")
        for warning in warnings:
            # Handle both dict format and string format
            if isinstance(warning, dict):
                title = warning.get("title", "Warning")
                message = warning.get("message", "")
                warning_type = warning.get("type", "warning")
                # Set color based on type
                if warning_type == "error":
                    pdf.set_text_color(200, 0, 0)
                elif warning_type == "warning":
                    pdf.set_text_color(200, 100, 0)
                else:  # info
                    pdf.set_text_color(100, 100, 200)
                pdf.set_font("Helvetica", "B", 9)
                pdf.cell(0, 5, f"! {title}", new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", "", 9)
                pdf.multi_cell(0, 5, f"  {message}")
            else:
                pdf.set_text_color(200, 100, 0)
                pdf.set_font("Helvetica", "", 9)
                pdf.multi_cell(0, 5, f"! {warning}")
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)

    # Disclaimer
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 4,
        "DISCLAIMER: This valuation is for informational purposes only and should not be considered "
        "as professional financial advice. Road tax rates are based on 2024-25 government sources "
        "and may have changed. Always verify the actual condition of the vehicle, check all documents, "
        "and consult with professionals before making a purchase decision."
    )

    # Output to bytes
    return bytes(pdf.output())

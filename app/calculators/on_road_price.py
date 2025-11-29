"""On-road price calculation module."""

from typing import Optional
from app.data.road_tax import get_road_tax_rate, get_slab_info
from app.data.constants import (
    FIXED_CHARGES,
    INSURANCE_ESTIMATES,
    HANDLING_CHARGES,
    TCS_THRESHOLD,
    TCS_RATE,
)
from app.data.gst import classify_gst_category, calculate_gst_component


def get_insurance_category(ex_showroom: float) -> str:
    """Determine insurance category based on ex-showroom price."""
    if ex_showroom < 600000:
        return "budget"
    elif ex_showroom < 1000000:
        return "hatchback"
    elif ex_showroom < 1400000:
        return "compact_suv"
    elif ex_showroom < 1800000:
        return "sedan"
    elif ex_showroom < 2500000:
        return "suv"
    elif ex_showroom < 4000000:
        return "premium_suv"
    else:
        return "luxury"


def get_handling_category(ex_showroom: float) -> str:
    """Determine handling charges category based on ex-showroom price."""
    if ex_showroom < 800000:
        return "budget"
    elif ex_showroom < 1200000:
        return "compact"
    elif ex_showroom < 1800000:
        return "mid"
    elif ex_showroom < 3000000:
        return "premium"
    else:
        return "luxury"


def calculate_road_tax(ex_showroom: float, state: str, fuel_type: str) -> float:
    """Calculate road tax amount."""
    rate = get_road_tax_rate(state, fuel_type, ex_showroom)
    return ex_showroom * rate


def calculate_insurance_estimate(ex_showroom: float) -> float:
    """Calculate estimated first-year insurance."""
    category = get_insurance_category(ex_showroom)
    return INSURANCE_ESTIMATES.get(category, INSURANCE_ESTIMATES["sedan"])


def calculate_handling_charges(ex_showroom: float) -> float:
    """Calculate dealer handling/logistics charges."""
    category = get_handling_category(ex_showroom)
    return HANDLING_CHARGES.get(category, HANDLING_CHARGES["mid"])


def calculate_tcs(ex_showroom: float) -> float:
    """
    Calculate TCS (Tax Collected at Source).
    TCS of 1% is applicable on cars with ex-showroom price > 10 lakh.
    """
    if ex_showroom > TCS_THRESHOLD:
        return ex_showroom * TCS_RATE
    return 0.0


def calculate_fixed_charges(has_loan: bool = False) -> float:
    """Calculate fixed charges (registration, HSRP, FasTag, RTO misc)."""
    total = (
        FIXED_CHARGES["registration"]
        + FIXED_CHARGES["hsrp"]
        + FIXED_CHARGES["fastag"]
        + FIXED_CHARGES["rto_misc"]
    )
    if has_loan:
        total += FIXED_CHARGES["hypothecation"]
    return total


def calculate_on_road_price(
    ex_showroom: float,
    state: str,
    fuel_type: str,
    has_loan: bool = False,
    custom_road_tax_rate: Optional[float] = None,
    engine_cc: Optional[int] = None,
    length_mm: Optional[int] = None,
) -> dict:
    """
    Calculate complete on-road price breakdown.

    Args:
        ex_showroom: Ex-showroom price in INR
        state: Registration state
        fuel_type: Fuel type of the car
        has_loan: Whether the car was purchased on loan
        custom_road_tax_rate: Optional custom road tax rate (as decimal, e.g., 0.12 for 12%)
        engine_cc: Optional engine capacity in CC (for GST classification)
        length_mm: Optional vehicle length in mm (for GST classification)

    Returns a dict with:
    - ex_showroom: Original ex-showroom price
    - road_tax: Road tax amount
    - road_tax_rate: Road tax percentage used
    - default_road_tax_rate: Default rate from database (for comparison)
    - is_custom_rate: Whether custom rate was used
    - slab_info: Detailed slab information (slab_name, slab_range, rate, rate_percent, reason)
    - insurance: Insurance estimate
    - fixed_charges: Registration, HSRP, FasTag, RTO misc
    - handling_charges: Dealer handling/logistics charges
    - tcs: Tax Collected at Source (1% if > 10L)
    - on_road_price: Total on-road price
    - gst_info: GST classification info (category, rate, reason)
    - gst_breakdown: GST component breakdown (base_price, gst_amount)
    """
    # Get detailed slab info from database
    slab_info = get_slab_info(state, fuel_type, ex_showroom)
    default_road_tax_rate = slab_info["rate"]

    # Use custom rate if provided, otherwise use default
    if custom_road_tax_rate is not None:
        road_tax_rate = custom_road_tax_rate
        is_custom_rate = True
        # Update slab_info to reflect custom rate
        slab_info = {
            **slab_info,
            "rate": custom_road_tax_rate,
            "rate_percent": f"{custom_road_tax_rate * 100:.1f}%",
            "reason": f"Custom road tax rate of {custom_road_tax_rate * 100:.1f}% applied (default for {state} {fuel_type} in {slab_info['slab_range']} is {default_road_tax_rate * 100:.1f}%)",
        }
    else:
        road_tax_rate = default_road_tax_rate
        is_custom_rate = False

    road_tax = ex_showroom * road_tax_rate
    insurance = calculate_insurance_estimate(ex_showroom)
    fixed_charges = calculate_fixed_charges(has_loan)
    handling_charges = calculate_handling_charges(ex_showroom)
    tcs = calculate_tcs(ex_showroom)

    on_road_price = ex_showroom + road_tax + insurance + fixed_charges + handling_charges + tcs

    # GST classification and breakdown
    gst_info = classify_gst_category(fuel_type, engine_cc, length_mm)
    gst_breakdown = calculate_gst_component(ex_showroom, gst_info["rate"])

    return {
        "ex_showroom": ex_showroom,
        "road_tax": road_tax,
        "road_tax_rate": road_tax_rate,
        "default_road_tax_rate": default_road_tax_rate,
        "is_custom_rate": is_custom_rate,
        "slab_info": slab_info,
        "insurance": insurance,
        "fixed_charges": fixed_charges,
        "handling_charges": handling_charges,
        "tcs": tcs,
        "on_road_price": on_road_price,
        "gst_info": gst_info,
        "gst_breakdown": gst_breakdown,
    }

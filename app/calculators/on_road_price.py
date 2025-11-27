"""On-road price calculation module."""

from app.data.road_tax import get_road_tax_rate
from app.data.constants import FIXED_CHARGES, INSURANCE_ESTIMATES


def get_insurance_category(ex_showroom: float) -> str:
    """Determine insurance category based on ex-showroom price."""
    if ex_showroom < 1000000:
        return "hatchback"
    elif ex_showroom < 1500000:
        return "sedan"
    elif ex_showroom < 2500000:
        return "suv"
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


def calculate_fixed_charges(has_loan: bool = False) -> float:
    """Calculate fixed charges (registration, HSRP, FasTag)."""
    total = (
        FIXED_CHARGES["registration"]
        + FIXED_CHARGES["hsrp"]
        + FIXED_CHARGES["fastag"]
    )
    if has_loan:
        total += FIXED_CHARGES["hypothecation"]
    return total


def calculate_on_road_price(
    ex_showroom: float,
    state: str,
    fuel_type: str,
    has_loan: bool = False,
) -> dict:
    """
    Calculate complete on-road price breakdown.

    Returns a dict with:
    - ex_showroom: Original ex-showroom price
    - road_tax: Road tax amount
    - road_tax_rate: Road tax percentage
    - insurance: Insurance estimate
    - fixed_charges: Registration, HSRP, FasTag
    - on_road_price: Total on-road price
    """
    road_tax = calculate_road_tax(ex_showroom, state, fuel_type)
    road_tax_rate = get_road_tax_rate(state, fuel_type, ex_showroom)
    insurance = calculate_insurance_estimate(ex_showroom)
    fixed_charges = calculate_fixed_charges(has_loan)

    on_road_price = ex_showroom + road_tax + insurance + fixed_charges

    return {
        "ex_showroom": ex_showroom,
        "road_tax": road_tax,
        "road_tax_rate": road_tax_rate,
        "insurance": insurance,
        "fixed_charges": fixed_charges,
        "on_road_price": on_road_price,
    }

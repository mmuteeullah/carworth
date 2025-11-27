"""Fair value calculation module."""

from app.data.constants import FAIR_VALUE_RANGE, INSURANCE_ESTIMATES


def get_insurance_cost(ex_showroom: float) -> float:
    """Get insurance cost for deduction if expired."""
    if ex_showroom < 1000000:
        return INSURANCE_ESTIMATES["hatchback"]
    elif ex_showroom < 1500000:
        return INSURANCE_ESTIMATES["sedan"]
    elif ex_showroom < 2500000:
        return INSURANCE_ESTIMATES["suv"]
    else:
        return INSURANCE_ESTIMATES["luxury"]


def calculate_fair_value(
    on_road_price: float,
    total_depreciation: float,
) -> float:
    """
    Calculate fair market value.

    Formula: Fair Value = On-Road Price × (1 - Total Depreciation)
    """
    return on_road_price * (1 - total_depreciation)


def calculate_fair_value_range(
    fair_value: float,
    range_percent: float = FAIR_VALUE_RANGE,
) -> tuple[float, float]:
    """
    Calculate fair value range (min, max).

    Default range is +/- 5% of fair value.
    """
    min_value = fair_value * (1 - range_percent)
    max_value = fair_value * (1 + range_percent)
    return min_value, max_value


def adjust_for_insurance(
    fair_value: float,
    insurance_valid: bool,
    ex_showroom: float,
) -> tuple[float, float]:
    """
    Adjust fair value for insurance status.

    If insurance is expired, deduct estimated insurance cost.

    Returns:
        tuple: (adjusted_fair_value, insurance_deduction)
    """
    if insurance_valid:
        return fair_value, 0.0

    insurance_cost = get_insurance_cost(ex_showroom)
    adjusted = fair_value - insurance_cost
    return adjusted, insurance_cost


def calculate_complete_fair_value(
    on_road_price: float,
    total_depreciation: float,
    insurance_valid: bool,
    ex_showroom: float,
) -> dict:
    """
    Calculate complete fair value with all adjustments.

    Returns dict with:
    - base_fair_value: Before insurance adjustment
    - insurance_deduction: Amount deducted for expired insurance
    - fair_value: Final fair value
    - fair_value_min: Lower bound of range
    - fair_value_max: Upper bound of range
    """
    base_fair_value = calculate_fair_value(on_road_price, total_depreciation)

    adjusted_value, insurance_deduction = adjust_for_insurance(
        base_fair_value, insurance_valid, ex_showroom
    )

    min_value, max_value = calculate_fair_value_range(adjusted_value)

    return {
        "base_fair_value": base_fair_value,
        "insurance_deduction": insurance_deduction,
        "fair_value": adjusted_value,
        "fair_value_min": min_value,
        "fair_value_max": max_value,
    }

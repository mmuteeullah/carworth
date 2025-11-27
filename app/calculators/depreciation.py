"""Depreciation calculation module."""

from app.data.road_tax import is_ncr_state
from app.data.brands import get_brand_multiplier
from app.data.constants import (
    CURRENT_YEAR,
    CAR_LIFE_YEARS,
    DIESEL_NCR_LIFE_YEARS,
    MAX_DEPRECIATION,
    OWNERSHIP_PREMIUM,
    TRANSMISSION_ADJUSTMENT,
    CONDITION_ADJUSTMENTS,
    EXPECTED_ANNUAL_KM,
    MILEAGE_THRESHOLDS,
    MILEAGE_ADJUSTMENTS,
)


def get_owner_number(owner_str: str) -> int:
    """Convert owner string to number."""
    mapping = {
        "1st Owner": 1,
        "2nd Owner": 2,
        "3rd Owner": 3,
        "4th+ Owner": 4,
    }
    return mapping.get(owner_str, 2)


def calculate_life_depreciation(
    year: int,
    fuel_type: str,
    state: str,
) -> tuple[float, int]:
    """
    Calculate life-based depreciation.

    Returns:
        tuple: (depreciation_rate, car_age)
    """
    age = CURRENT_YEAR - year

    # Diesel cars in NCR have 10-year life
    if fuel_type == "Diesel" and is_ncr_state(state):
        life_years = DIESEL_NCR_LIFE_YEARS
    else:
        life_years = CAR_LIFE_YEARS

    depreciation = age / life_years

    return depreciation, age


def calculate_ownership_premium(owner_number: int) -> float:
    """Calculate ownership premium based on owner number."""
    if owner_number >= 4:
        return OWNERSHIP_PREMIUM[4]
    return OWNERSHIP_PREMIUM.get(owner_number, OWNERSHIP_PREMIUM[2])


def calculate_mileage_adjustment(km: int, age: int) -> tuple[float, str]:
    """
    Calculate mileage-based adjustment.

    Returns:
        tuple: (adjustment_rate, mileage_status)
    """
    if age <= 0:
        expected_km = EXPECTED_ANNUAL_KM
    else:
        expected_km = age * EXPECTED_ANNUAL_KM

    if km > expected_km * MILEAGE_THRESHOLDS["high"]:
        return MILEAGE_ADJUSTMENTS["high"], "high"
    elif km > expected_km * MILEAGE_THRESHOLDS["slight_high"]:
        return MILEAGE_ADJUSTMENTS["slight_high"], "slightly_high"
    elif km < expected_km * MILEAGE_THRESHOLDS["very_low"]:
        return 0.0, "very_low"  # Warning but no adjustment
    else:
        return 0.0, "normal"


def apply_brand_multiplier(base_depreciation: float, brand: str) -> float:
    """Apply brand-specific multiplier to depreciation."""
    multiplier = get_brand_multiplier(brand)
    return base_depreciation * multiplier


def calculate_transmission_adjustment(transmission: str) -> float:
    """Get transmission-based adjustment."""
    return TRANSMISSION_ADJUSTMENT.get(transmission, 0.0)


def calculate_condition_adjustment(
    body_condition: str = "Good",
    accident_history: str = "None",
    service_history: str = "Unknown",
    commercial_use: bool = False,
    new_gen_available: bool = False,
) -> dict:
    """
    Calculate condition-based adjustments.

    Returns dict with individual adjustments and total.
    """
    body_adj = CONDITION_ADJUSTMENTS["body"].get(body_condition, 0.0)
    accident_adj = CONDITION_ADJUSTMENTS["accident"].get(accident_history, 0.0)
    service_adj = CONDITION_ADJUSTMENTS["service"].get(service_history, 0.0)
    commercial_adj = CONDITION_ADJUSTMENTS["commercial"] if commercial_use else 0.0
    new_gen_adj = CONDITION_ADJUSTMENTS["new_gen_available"] if new_gen_available else 0.0

    return {
        "body": body_adj,
        "accident": accident_adj,
        "service": service_adj,
        "commercial": commercial_adj,
        "new_gen": new_gen_adj,
        "total": body_adj + accident_adj + service_adj + commercial_adj + new_gen_adj,
    }


def calculate_total_depreciation(
    year: int,
    fuel_type: str,
    state: str,
    owner: str,
    km: int,
    brand: str = "Other",
    transmission: str = "Manual",
    body_condition: str = "Good",
    accident_history: str = "None",
    service_history: str = "Unknown",
    commercial_use: bool = False,
    new_gen_available: bool = False,
) -> dict:
    """
    Calculate total depreciation with full breakdown.

    Returns dict with all components and final depreciation rate.
    """
    owner_number = get_owner_number(owner)

    # Life depreciation
    life_dep, age = calculate_life_depreciation(year, fuel_type, state)

    # Apply brand multiplier to life depreciation
    branded_life_dep = apply_brand_multiplier(life_dep, brand)

    # Ownership premium
    ownership_dep = calculate_ownership_premium(owner_number)

    # Mileage adjustment
    mileage_adj, mileage_status = calculate_mileage_adjustment(km, age)

    # Transmission adjustment
    transmission_adj = calculate_transmission_adjustment(transmission)

    # Condition adjustments
    condition = calculate_condition_adjustment(
        body_condition=body_condition,
        accident_history=accident_history,
        service_history=service_history,
        commercial_use=commercial_use,
        new_gen_available=new_gen_available,
    )

    # Total depreciation (before cap)
    total_raw = (
        branded_life_dep
        + ownership_dep
        + mileage_adj
        + transmission_adj
        + condition["total"]
    )

    # Apply cap
    total_capped = min(total_raw, MAX_DEPRECIATION)

    return {
        "age": age,
        "life_depreciation": life_dep,
        "brand_multiplier": get_brand_multiplier(brand),
        "branded_life_depreciation": branded_life_dep,
        "ownership_premium": ownership_dep,
        "mileage_adjustment": mileage_adj,
        "mileage_status": mileage_status,
        "transmission_adjustment": transmission_adj,
        "condition_adjustments": condition,
        "total_raw": total_raw,
        "total_capped": total_capped,
        "is_capped": total_raw > MAX_DEPRECIATION,
    }

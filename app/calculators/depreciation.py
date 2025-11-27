"""Depreciation calculation module.

Basic Formula (from YouTube videos - works for 80% of cases):
    Total Depreciation = Life Depreciation + Ownership Premium + Mileage Adjustment

    Where:
    - Life Depreciation = Age / 15 years (or Age / 10 for Diesel in NCR)
    - Ownership Premium = 10% (1st) / 15% (2nd) / 20% (3rd) / 30% (4th+)
    - Mileage Adjustment = +2% if slightly high, +5% if high

Advanced Adjustments (edge cases for special situations):
    - Brand Multiplier: Maruti/Toyota 0.85x, Skoda/VW 1.15x, Luxury 1.25x
    - Transmission: DCT/DSG +5%, AMT +2%
    - Condition: Body, Accident history, Service history
    - Commercial use: +15%
    - New generation available: +5%
"""

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
) -> tuple[float, int, int]:
    """
    Calculate life-based depreciation.

    Returns:
        tuple: (depreciation_rate, car_age, life_years_used)
    """
    age = CURRENT_YEAR - year

    # Diesel cars in NCR have 10-year life
    if fuel_type == "Diesel" and is_ncr_state(state):
        life_years = DIESEL_NCR_LIFE_YEARS
    else:
        life_years = CAR_LIFE_YEARS

    depreciation = age / life_years

    return depreciation, age, life_years


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


def calculate_brand_adjustment(life_dep: float, brand: str) -> tuple[float, float]:
    """
    Calculate brand-based adjustment to life depreciation.

    Returns:
        tuple: (adjustment_amount, multiplier)
    """
    multiplier = get_brand_multiplier(brand)
    # Adjustment is the difference from applying multiplier
    adjustment = life_dep * (multiplier - 1.0)
    return adjustment, multiplier


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

    Separates Basic (video formula) vs Advanced (edge case) adjustments.

    Returns dict with all components and final depreciation rates.
    """
    owner_number = get_owner_number(owner)

    # === BASIC FORMULA (from videos) ===
    # Life depreciation
    life_dep, age, life_years = calculate_life_depreciation(year, fuel_type, state)

    # Ownership premium
    ownership_dep = calculate_ownership_premium(owner_number)

    # Mileage adjustment
    mileage_adj, mileage_status = calculate_mileage_adjustment(km, age)

    # Basic total (the "video formula")
    basic_total = life_dep + ownership_dep + mileage_adj
    basic_capped = min(basic_total, MAX_DEPRECIATION)

    # === ADVANCED ADJUSTMENTS (edge cases) ===
    # Brand adjustment
    brand_adj, brand_multiplier = calculate_brand_adjustment(life_dep, brand)

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

    # Advanced total = basic + all edge case adjustments
    advanced_adjustments = brand_adj + transmission_adj + condition["total"]
    advanced_total = basic_total + advanced_adjustments
    advanced_capped = min(advanced_total, MAX_DEPRECIATION)

    return {
        "age": age,
        "life_years": life_years,
        # Basic formula components
        "life_depreciation": life_dep,
        "ownership_premium": ownership_dep,
        "mileage_adjustment": mileage_adj,
        "mileage_status": mileage_status,
        # Basic totals
        "basic_total": basic_total,
        "basic_capped": basic_capped,
        "basic_is_capped": basic_total > MAX_DEPRECIATION,
        # Advanced adjustments
        "brand_adjustment": brand_adj,
        "brand_multiplier": brand_multiplier,
        "transmission_adjustment": transmission_adj,
        "condition_adjustments": condition,
        # Advanced totals
        "advanced_adjustments_total": advanced_adjustments,
        "advanced_total": advanced_total,
        "advanced_capped": advanced_capped,
        "advanced_is_capped": advanced_total > MAX_DEPRECIATION,
        # Legacy fields for backward compatibility
        "total_raw": advanced_total,
        "total_capped": advanced_capped,
        "is_capped": advanced_total > MAX_DEPRECIATION,
    }

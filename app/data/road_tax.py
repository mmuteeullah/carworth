"""State-wise road tax data for India."""

from typing import Literal

FuelType = Literal["Petrol", "Diesel", "CNG", "Electric", "Hybrid"]
PriceCategory = Literal["budget", "mid", "premium"]

ROAD_TAX_RATES: dict[str, dict[str, dict[str, float]]] = {
    "Delhi": {
        "Petrol": {"budget": 0.055, "mid": 0.085, "premium": 0.10},
        "Diesel": {"budget": 0.07, "mid": 0.105, "premium": 0.125},
        "CNG": {"budget": 0.04, "mid": 0.06, "premium": 0.08},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.04, "mid": 0.06, "premium": 0.08},
    },
    "Haryana": {
        "Petrol": {"budget": 0.05, "mid": 0.08, "premium": 0.10},
        "Diesel": {"budget": 0.06, "mid": 0.09, "premium": 0.11},
        "CNG": {"budget": 0.04, "mid": 0.06, "premium": 0.08},
        "Electric": {"budget": 0.02, "mid": 0.02, "premium": 0.02},
        "Hybrid": {"budget": 0.04, "mid": 0.06, "premium": 0.08},
    },
    "Maharashtra": {
        "Petrol": {"budget": 0.11, "mid": 0.12, "premium": 0.13},
        "Diesel": {"budget": 0.13, "mid": 0.14, "premium": 0.15},
        "CNG": {"budget": 0.07, "mid": 0.08, "premium": 0.09},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.09, "mid": 0.10, "premium": 0.11},
    },
    "Karnataka": {
        "Petrol": {"budget": 0.13, "mid": 0.17, "premium": 0.18},
        "Diesel": {"budget": 0.14, "mid": 0.17, "premium": 0.18},
        "CNG": {"budget": 0.10, "mid": 0.13, "premium": 0.14},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.10, "mid": 0.13, "premium": 0.14},
    },
    "Telangana": {
        "Petrol": {"budget": 0.13, "mid": 0.17, "premium": 0.18},
        "Diesel": {"budget": 0.14, "mid": 0.17, "premium": 0.18},
        "CNG": {"budget": 0.10, "mid": 0.13, "premium": 0.14},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.10, "mid": 0.13, "premium": 0.14},
    },
    "Tamil Nadu": {
        "Petrol": {"budget": 0.10, "mid": 0.15, "premium": 0.15},
        "Diesel": {"budget": 0.10, "mid": 0.15, "premium": 0.15},
        "CNG": {"budget": 0.07, "mid": 0.10, "premium": 0.10},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.07, "mid": 0.10, "premium": 0.10},
    },
    "Uttar Pradesh": {
        "Petrol": {"budget": 0.08, "mid": 0.10, "premium": 0.10},
        "Diesel": {"budget": 0.08, "mid": 0.10, "premium": 0.10},
        "CNG": {"budget": 0.06, "mid": 0.07, "premium": 0.08},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.06, "mid": 0.08, "premium": 0.08},
    },
    "Gujarat": {
        "Petrol": {"budget": 0.06, "mid": 0.06, "premium": 0.06},
        "Diesel": {"budget": 0.06, "mid": 0.06, "premium": 0.06},
        "CNG": {"budget": 0.04, "mid": 0.04, "premium": 0.04},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.04, "mid": 0.04, "premium": 0.04},
    },
    "Rajasthan": {
        "Petrol": {"budget": 0.08, "mid": 0.10, "premium": 0.11},
        "Diesel": {"budget": 0.09, "mid": 0.11, "premium": 0.12},
        "CNG": {"budget": 0.06, "mid": 0.07, "premium": 0.08},
        "Electric": {"budget": 0.02, "mid": 0.02, "premium": 0.02},
        "Hybrid": {"budget": 0.06, "mid": 0.08, "premium": 0.09},
    },
    "Punjab": {
        "Petrol": {"budget": 0.09, "mid": 0.11, "premium": 0.12},
        "Diesel": {"budget": 0.10, "mid": 0.12, "premium": 0.13},
        "CNG": {"budget": 0.06, "mid": 0.08, "premium": 0.09},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.07, "mid": 0.09, "premium": 0.10},
    },
    "West Bengal": {
        "Petrol": {"budget": 0.10, "mid": 0.12, "premium": 0.14},
        "Diesel": {"budget": 0.12, "mid": 0.14, "premium": 0.16},
        "CNG": {"budget": 0.07, "mid": 0.09, "premium": 0.10},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.08, "mid": 0.10, "premium": 0.12},
    },
    "Kerala": {
        "Petrol": {"budget": 0.09, "mid": 0.12, "premium": 0.15},
        "Diesel": {"budget": 0.10, "mid": 0.13, "premium": 0.16},
        "CNG": {"budget": 0.06, "mid": 0.08, "premium": 0.10},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.07, "mid": 0.10, "premium": 0.12},
    },
    "Madhya Pradesh": {
        "Petrol": {"budget": 0.08, "mid": 0.10, "premium": 0.12},
        "Diesel": {"budget": 0.09, "mid": 0.11, "premium": 0.13},
        "CNG": {"budget": 0.05, "mid": 0.07, "premium": 0.08},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.06, "mid": 0.08, "premium": 0.10},
    },
    "Bihar": {
        "Petrol": {"budget": 0.07, "mid": 0.09, "premium": 0.10},
        "Diesel": {"budget": 0.08, "mid": 0.10, "premium": 0.11},
        "CNG": {"budget": 0.05, "mid": 0.06, "premium": 0.07},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.05, "mid": 0.07, "premium": 0.08},
    },
    "Odisha": {
        "Petrol": {"budget": 0.07, "mid": 0.09, "premium": 0.10},
        "Diesel": {"budget": 0.08, "mid": 0.10, "premium": 0.11},
        "CNG": {"budget": 0.05, "mid": 0.06, "premium": 0.07},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.05, "mid": 0.07, "premium": 0.08},
    },
    "Andhra Pradesh": {
        "Petrol": {"budget": 0.12, "mid": 0.14, "premium": 0.16},
        "Diesel": {"budget": 0.13, "mid": 0.15, "premium": 0.17},
        "CNG": {"budget": 0.08, "mid": 0.10, "premium": 0.12},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.10, "mid": 0.12, "premium": 0.14},
    },
    "Jharkhand": {
        "Petrol": {"budget": 0.06, "mid": 0.08, "premium": 0.10},
        "Diesel": {"budget": 0.07, "mid": 0.09, "premium": 0.11},
        "CNG": {"budget": 0.04, "mid": 0.06, "premium": 0.07},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.05, "mid": 0.07, "premium": 0.08},
    },
    "Chhattisgarh": {
        "Petrol": {"budget": 0.07, "mid": 0.09, "premium": 0.10},
        "Diesel": {"budget": 0.08, "mid": 0.10, "premium": 0.11},
        "CNG": {"budget": 0.05, "mid": 0.06, "premium": 0.07},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.05, "mid": 0.07, "premium": 0.08},
    },
    "Uttarakhand": {
        "Petrol": {"budget": 0.07, "mid": 0.08, "premium": 0.09},
        "Diesel": {"budget": 0.08, "mid": 0.09, "premium": 0.10},
        "CNG": {"budget": 0.05, "mid": 0.06, "premium": 0.07},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.05, "mid": 0.06, "premium": 0.07},
    },
    "Himachal Pradesh": {
        "Petrol": {"budget": 0.06, "mid": 0.07, "premium": 0.08},
        "Diesel": {"budget": 0.07, "mid": 0.08, "premium": 0.09},
        "CNG": {"budget": 0.04, "mid": 0.05, "premium": 0.06},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.04, "mid": 0.05, "premium": 0.06},
    },
    "Assam": {
        "Petrol": {"budget": 0.07, "mid": 0.09, "premium": 0.10},
        "Diesel": {"budget": 0.08, "mid": 0.10, "premium": 0.11},
        "CNG": {"budget": 0.05, "mid": 0.06, "premium": 0.07},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.05, "mid": 0.07, "premium": 0.08},
    },
    "Goa": {
        "Petrol": {"budget": 0.09, "mid": 0.11, "premium": 0.13},
        "Diesel": {"budget": 0.10, "mid": 0.12, "premium": 0.14},
        "CNG": {"budget": 0.06, "mid": 0.08, "premium": 0.09},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.07, "mid": 0.09, "premium": 0.11},
    },
    "Chandigarh": {
        "Petrol": {"budget": 0.04, "mid": 0.06, "premium": 0.07},
        "Diesel": {"budget": 0.05, "mid": 0.07, "premium": 0.08},
        "CNG": {"budget": 0.03, "mid": 0.04, "premium": 0.05},
        "Electric": {"budget": 0.0, "mid": 0.0, "premium": 0.0},
        "Hybrid": {"budget": 0.03, "mid": 0.05, "premium": 0.06},
    },
}

# NCR states for diesel 10-year rule
NCR_STATES = ["Delhi", "Haryana", "Uttar Pradesh", "Rajasthan"]


def get_price_category(ex_showroom: float) -> PriceCategory:
    """Determine price category based on ex-showroom price."""
    if ex_showroom < 1000000:  # Less than 10 lakh
        return "budget"
    elif ex_showroom < 2000000:  # 10-20 lakh
        return "mid"
    else:  # More than 20 lakh
        return "premium"


def get_road_tax_rate(
    state: str, fuel_type: FuelType, ex_showroom: float
) -> float:
    """Get road tax rate for given state, fuel type and price category."""
    category = get_price_category(ex_showroom)

    if state not in ROAD_TAX_RATES:
        # Default to Maharashtra rates if state not found
        state = "Maharashtra"

    state_rates = ROAD_TAX_RATES[state]
    fuel_rates = state_rates.get(fuel_type, state_rates["Petrol"])

    return fuel_rates.get(category, fuel_rates["mid"])


def is_ncr_state(state: str) -> bool:
    """Check if state is in NCR region."""
    return state in NCR_STATES

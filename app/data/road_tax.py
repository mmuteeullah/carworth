"""State-wise road tax data for India with accurate state-specific slabs."""

from typing import Literal, TypedDict

FuelType = Literal["Petrol", "Diesel", "CNG", "Electric", "Hybrid"]


class SlabInfo(TypedDict):
    """Information about the applied tax slab."""
    slab_name: str
    slab_range: str
    rate: float
    rate_percent: str
    reason: str


class StateSlabConfig(TypedDict):
    """Configuration for a state's tax slabs."""
    slabs: list[tuple[float, str, str]]  # (upper_limit, slab_name, range_description)
    rates: dict[str, dict[str, float]]  # fuel_type -> slab_name -> rate


# State-specific slab configurations
# Each state has its own slab boundaries and rates per fuel type
STATE_TAX_CONFIG: dict[str, StateSlabConfig] = {
    "Delhi": {
        # Delhi uses ₹6L and ₹10L boundaries
        "slabs": [
            (600000, "slab1", "Up to ₹6 Lakh"),
            (1000000, "slab2", "₹6-10 Lakh"),
            (float("inf"), "slab3", "Above ₹10 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.04, "slab2": 0.07, "slab3": 0.10},
            "Diesel": {"slab1": 0.05, "slab2": 0.0875, "slab3": 0.125},
            "CNG": {"slab1": 0.04, "slab2": 0.06, "slab3": 0.08},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.04, "slab2": 0.06, "slab3": 0.08},
        },
    },
    "Haryana": {
        # Haryana uses ₹6L and ₹20L boundaries
        "slabs": [
            (600000, "slab1", "Up to ₹6 Lakh"),
            (2000000, "slab2", "₹6-20 Lakh"),
            (float("inf"), "slab3", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.05, "slab2": 0.08, "slab3": 0.10},
            "Diesel": {"slab1": 0.06, "slab2": 0.09, "slab3": 0.11},
            "CNG": {"slab1": 0.04, "slab2": 0.064, "slab3": 0.08},  # 20% rebate on petrol
            "Electric": {"slab1": 0.02, "slab2": 0.02, "slab3": 0.02},
            "Hybrid": {"slab1": 0.04, "slab2": 0.064, "slab3": 0.08},
        },
    },
    "Maharashtra": {
        # Maharashtra uses ₹10L and ₹20L boundaries
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (2000000, "slab2", "₹10-20 Lakh"),
            (float("inf"), "slab3", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.11, "slab2": 0.12, "slab3": 0.13},
            "Diesel": {"slab1": 0.13, "slab2": 0.14, "slab3": 0.15},
            "CNG": {"slab1": 0.07, "slab2": 0.08, "slab3": 0.09},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.09, "slab2": 0.10, "slab3": 0.11},
        },
    },
    "Karnataka": {
        # Karnataka uses ₹5L, ₹10L, ₹20L boundaries (highest rates in India)
        "slabs": [
            (500000, "slab1", "Up to ₹5 Lakh"),
            (1000000, "slab2", "₹5-10 Lakh"),
            (2000000, "slab3", "₹10-20 Lakh"),
            (float("inf"), "slab4", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.13, "slab2": 0.14, "slab3": 0.17, "slab4": 0.18},
            "Diesel": {"slab1": 0.13, "slab2": 0.14, "slab3": 0.17, "slab4": 0.18},
            "CNG": {"slab1": 0.10, "slab2": 0.11, "slab3": 0.13, "slab4": 0.14},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0, "slab4": 0.0},
            "Hybrid": {"slab1": 0.10, "slab2": 0.11, "slab3": 0.13, "slab4": 0.14},
        },
    },
    "Telangana": {
        # Telangana uses ₹10L boundary
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (float("inf"), "slab2", "Above ₹10 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.12, "slab2": 0.14},
            "Diesel": {"slab1": 0.12, "slab2": 0.14},
            "CNG": {"slab1": 0.10, "slab2": 0.12},
            "Electric": {"slab1": 0.0, "slab2": 0.0},
            "Hybrid": {"slab1": 0.10, "slab2": 0.12},
        },
    },
    "Andhra Pradesh": {
        # Andhra Pradesh uses ₹10L boundary
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (float("inf"), "slab2", "Above ₹10 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.12, "slab2": 0.14},
            "Diesel": {"slab1": 0.13, "slab2": 0.15},
            "CNG": {"slab1": 0.08, "slab2": 0.10},
            "Electric": {"slab1": 0.0, "slab2": 0.0},
            "Hybrid": {"slab1": 0.10, "slab2": 0.12},
        },
    },
    "Tamil Nadu": {
        # Tamil Nadu uses ₹10L boundary
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (float("inf"), "slab2", "Above ₹10 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.10, "slab2": 0.15},
            "Diesel": {"slab1": 0.10, "slab2": 0.15},
            "CNG": {"slab1": 0.07, "slab2": 0.10},
            "Electric": {"slab1": 0.0, "slab2": 0.0},
            "Hybrid": {"slab1": 0.07, "slab2": 0.10},
        },
    },
    "Uttar Pradesh": {
        # UP uses ₹10L boundary
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (float("inf"), "slab2", "Above ₹10 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.08, "slab2": 0.10},
            "Diesel": {"slab1": 0.08, "slab2": 0.10},
            "CNG": {"slab1": 0.06, "slab2": 0.08},
            "Electric": {"slab1": 0.0, "slab2": 0.0},
            "Hybrid": {"slab1": 0.06, "slab2": 0.08},
        },
    },
    "Gujarat": {
        # Gujarat has flat 6% rate for all
        "slabs": [
            (float("inf"), "flat", "All Vehicles"),
        ],
        "rates": {
            "Petrol": {"flat": 0.06},
            "Diesel": {"flat": 0.06},
            "CNG": {"flat": 0.04},
            "Electric": {"flat": 0.0},
            "Hybrid": {"flat": 0.04},
        },
    },
    "Rajasthan": {
        # Rajasthan rates based on fuel type
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (2000000, "slab2", "₹10-20 Lakh"),
            (float("inf"), "slab3", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.06, "slab2": 0.07, "slab3": 0.08},
            "Diesel": {"slab1": 0.08, "slab2": 0.09, "slab3": 0.10},
            "CNG": {"slab1": 0.05, "slab2": 0.06, "slab3": 0.07},
            "Electric": {"slab1": 0.02, "slab2": 0.02, "slab3": 0.02},
            "Hybrid": {"slab1": 0.05, "slab2": 0.06, "slab3": 0.07},
        },
    },
    "Punjab": {
        # Punjab 8% + 1% social security
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (2000000, "slab2", "₹10-20 Lakh"),
            (float("inf"), "slab3", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.09, "slab2": 0.11, "slab3": 0.12},  # includes 1% social security
            "Diesel": {"slab1": 0.10, "slab2": 0.12, "slab3": 0.13},
            "CNG": {"slab1": 0.06, "slab2": 0.08, "slab3": 0.09},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.07, "slab2": 0.09, "slab3": 0.10},
        },
    },
    "West Bengal": {
        # West Bengal
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (2000000, "slab2", "₹10-20 Lakh"),
            (float("inf"), "slab3", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.10, "slab2": 0.12, "slab3": 0.14},
            "Diesel": {"slab1": 0.12, "slab2": 0.14, "slab3": 0.16},
            "CNG": {"slab1": 0.07, "slab2": 0.09, "slab3": 0.10},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.08, "slab2": 0.10, "slab3": 0.12},
        },
    },
    "Kerala": {
        # Kerala uses ₹5L, ₹10L, ₹15L boundaries
        "slabs": [
            (500000, "slab1", "Up to ₹5 Lakh"),
            (1000000, "slab2", "₹5-10 Lakh"),
            (1500000, "slab3", "₹10-15 Lakh"),
            (float("inf"), "slab4", "Above ₹15 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.06, "slab2": 0.08, "slab3": 0.10, "slab4": 0.12},
            "Diesel": {"slab1": 0.07, "slab2": 0.09, "slab3": 0.11, "slab4": 0.13},
            "CNG": {"slab1": 0.05, "slab2": 0.06, "slab3": 0.08, "slab4": 0.10},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0, "slab4": 0.0},
            "Hybrid": {"slab1": 0.05, "slab2": 0.07, "slab3": 0.09, "slab4": 0.11},
        },
    },
    "Madhya Pradesh": {
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (2000000, "slab2", "₹10-20 Lakh"),
            (float("inf"), "slab3", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.08, "slab2": 0.10, "slab3": 0.12},
            "Diesel": {"slab1": 0.09, "slab2": 0.11, "slab3": 0.13},
            "CNG": {"slab1": 0.05, "slab2": 0.07, "slab3": 0.08},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.06, "slab2": 0.08, "slab3": 0.10},
        },
    },
    "Bihar": {
        # Bihar uses ₹8L boundary
        "slabs": [
            (800000, "slab1", "Up to ₹8 Lakh"),
            (1500000, "slab2", "₹8-15 Lakh"),
            (float("inf"), "slab3", "Above ₹15 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.07, "slab2": 0.09, "slab3": 0.10},
            "Diesel": {"slab1": 0.08, "slab2": 0.10, "slab3": 0.11},
            "CNG": {"slab1": 0.05, "slab2": 0.06, "slab3": 0.07},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.05, "slab2": 0.07, "slab3": 0.08},
        },
    },
    "Odisha": {
        # Odisha uses ₹5L boundary
        "slabs": [
            (500000, "slab1", "Up to ₹5 Lakh"),
            (1000000, "slab2", "₹5-10 Lakh"),
            (float("inf"), "slab3", "Above ₹10 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.06, "slab2": 0.07, "slab3": 0.09},
            "Diesel": {"slab1": 0.06, "slab2": 0.07, "slab3": 0.09},
            "CNG": {"slab1": 0.05, "slab2": 0.06, "slab3": 0.07},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.05, "slab2": 0.06, "slab3": 0.07},
        },
    },
    "Jharkhand": {
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (2000000, "slab2", "₹10-20 Lakh"),
            (float("inf"), "slab3", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.06, "slab2": 0.08, "slab3": 0.10},
            "Diesel": {"slab1": 0.07, "slab2": 0.09, "slab3": 0.11},
            "CNG": {"slab1": 0.04, "slab2": 0.06, "slab3": 0.07},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.05, "slab2": 0.07, "slab3": 0.08},
        },
    },
    "Chhattisgarh": {
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (2000000, "slab2", "₹10-20 Lakh"),
            (float("inf"), "slab3", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.07, "slab2": 0.09, "slab3": 0.10},
            "Diesel": {"slab1": 0.08, "slab2": 0.10, "slab3": 0.11},
            "CNG": {"slab1": 0.05, "slab2": 0.06, "slab3": 0.07},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.05, "slab2": 0.07, "slab3": 0.08},
        },
    },
    "Uttarakhand": {
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (2000000, "slab2", "₹10-20 Lakh"),
            (float("inf"), "slab3", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.07, "slab2": 0.08, "slab3": 0.09},
            "Diesel": {"slab1": 0.08, "slab2": 0.09, "slab3": 0.10},
            "CNG": {"slab1": 0.05, "slab2": 0.06, "slab3": 0.07},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.05, "slab2": 0.06, "slab3": 0.07},
        },
    },
    "Himachal Pradesh": {
        # Himachal Pradesh - lowest rates in India (based on engine capacity, simplified to price)
        "slabs": [
            (800000, "slab1", "Up to ₹8 Lakh"),
            (1500000, "slab2", "₹8-15 Lakh"),
            (float("inf"), "slab3", "Above ₹15 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.025, "slab2": 0.03, "slab3": 0.04},
            "Diesel": {"slab1": 0.03, "slab2": 0.035, "slab3": 0.045},
            "CNG": {"slab1": 0.02, "slab2": 0.025, "slab3": 0.03},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.02, "slab2": 0.025, "slab3": 0.03},
        },
    },
    "Assam": {
        # Assam
        "slabs": [
            (500000, "slab1", "Up to ₹5 Lakh"),
            (1000000, "slab2", "₹5-10 Lakh"),
            (float("inf"), "slab3", "Above ₹10 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.04, "slab2": 0.06, "slab3": 0.07},
            "Diesel": {"slab1": 0.05, "slab2": 0.06, "slab3": 0.07},
            "CNG": {"slab1": 0.03, "slab2": 0.05, "slab3": 0.06},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.03, "slab2": 0.05, "slab3": 0.06},
        },
    },
    "Goa": {
        "slabs": [
            (1000000, "slab1", "Up to ₹10 Lakh"),
            (2000000, "slab2", "₹10-20 Lakh"),
            (float("inf"), "slab3", "Above ₹20 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.09, "slab2": 0.11, "slab3": 0.13},
            "Diesel": {"slab1": 0.10, "slab2": 0.12, "slab3": 0.14},
            "CNG": {"slab1": 0.06, "slab2": 0.08, "slab3": 0.09},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.07, "slab2": 0.09, "slab3": 0.11},
        },
    },
    "Chandigarh": {
        # Chandigarh - Union Territory with low rates
        "slabs": [
            (600000, "slab1", "Up to ₹6 Lakh"),
            (1000000, "slab2", "₹6-10 Lakh"),
            (float("inf"), "slab3", "Above ₹10 Lakh"),
        ],
        "rates": {
            "Petrol": {"slab1": 0.04, "slab2": 0.06, "slab3": 0.07},
            "Diesel": {"slab1": 0.05, "slab2": 0.07, "slab3": 0.08},
            "CNG": {"slab1": 0.03, "slab2": 0.04, "slab3": 0.05},
            "Electric": {"slab1": 0.0, "slab2": 0.0, "slab3": 0.0},
            "Hybrid": {"slab1": 0.03, "slab2": 0.05, "slab3": 0.06},
        },
    },
}

# NCR states for diesel 10-year rule
NCR_STATES = ["Delhi", "Haryana", "Uttar Pradesh", "Rajasthan"]

# Default state if not found
DEFAULT_STATE = "Maharashtra"


def get_slab_info(state: str, fuel_type: str, ex_showroom: float) -> SlabInfo:
    """
    Get detailed slab information for the given parameters.

    Returns a SlabInfo dict with:
    - slab_name: Internal slab identifier
    - slab_range: Human-readable price range
    - rate: Decimal rate (e.g., 0.11 for 11%)
    - rate_percent: Formatted percentage string
    - reason: Explanation of why this rate applies
    """
    if state not in STATE_TAX_CONFIG:
        state = DEFAULT_STATE

    config = STATE_TAX_CONFIG[state]
    slabs = config["slabs"]
    rates = config["rates"]

    # Find applicable slab
    applied_slab_name = None
    applied_slab_range = None

    for upper_limit, slab_name, slab_range in slabs:
        if ex_showroom <= upper_limit:
            applied_slab_name = slab_name
            applied_slab_range = slab_range
            break

    # If no slab found (shouldn't happen), use the last one
    if applied_slab_name is None:
        applied_slab_name = slabs[-1][1]
        applied_slab_range = slabs[-1][2]

    # Get fuel-specific rates, fallback to Petrol
    fuel_rates = rates.get(fuel_type, rates["Petrol"])
    rate = fuel_rates.get(applied_slab_name, 0.10)

    rate_percent = f"{rate * 100:.1f}%"

    # Build reason string
    reason = f"{state} charges {rate_percent} road tax for {fuel_type} vehicles in the {applied_slab_range} price bracket"

    return SlabInfo(
        slab_name=applied_slab_name,
        slab_range=applied_slab_range,
        rate=rate,
        rate_percent=rate_percent,
        reason=reason,
    )


def get_road_tax_rate(state: str, fuel_type: str, ex_showroom: float) -> float:
    """Get road tax rate for given state, fuel type and ex-showroom price."""
    slab_info = get_slab_info(state, fuel_type, ex_showroom)
    return slab_info["rate"]


def is_ncr_state(state: str) -> bool:
    """Check if state is in NCR region."""
    return state in NCR_STATES


def get_all_states() -> list[str]:
    """Get list of all supported states."""
    return list(STATE_TAX_CONFIG.keys())


def get_state_tax_table(state: str) -> dict:
    """
    Get complete tax table for a state.

    Returns dict with:
    - state: State name
    - slabs: List of slab ranges
    - rates: Dict of fuel_type -> list of rates per slab
    """
    if state not in STATE_TAX_CONFIG:
        state = DEFAULT_STATE

    config = STATE_TAX_CONFIG[state]
    slab_ranges = [slab[2] for slab in config["slabs"]]
    slab_names = [slab[1] for slab in config["slabs"]]

    rates_by_fuel = {}
    for fuel_type, fuel_rates in config["rates"].items():
        rates_by_fuel[fuel_type] = [
            f"{fuel_rates.get(slab_name, 0) * 100:.1f}%"
            for slab_name in slab_names
        ]

    return {
        "state": state,
        "slabs": slab_ranges,
        "rates": rates_by_fuel,
    }


def get_all_states_summary() -> list[dict]:
    """
    Get summary of all states with their tax ranges.

    Returns list of dicts with:
    - state: State name
    - petrol_range: "X% - Y%" range for petrol
    - diesel_range: "X% - Y%" range for diesel
    - electric_rate: Rate for EVs
    - num_slabs: Number of price slabs
    """
    summary = []

    for state, config in STATE_TAX_CONFIG.items():
        petrol_rates = list(config["rates"]["Petrol"].values())
        diesel_rates = list(config["rates"]["Diesel"].values())
        electric_rates = list(config["rates"]["Electric"].values())

        petrol_min = min(petrol_rates) * 100
        petrol_max = max(petrol_rates) * 100
        diesel_min = min(diesel_rates) * 100
        diesel_max = max(diesel_rates) * 100
        electric_rate = max(electric_rates) * 100

        summary.append({
            "state": state,
            "petrol_range": f"{petrol_min:.1f}% - {petrol_max:.1f}%" if petrol_min != petrol_max else f"{petrol_min:.1f}%",
            "diesel_range": f"{diesel_min:.1f}% - {diesel_max:.1f}%" if diesel_min != diesel_max else f"{diesel_min:.1f}%",
            "electric_rate": f"{electric_rate:.1f}%",
            "num_slabs": len(config["slabs"]),
        })

    # Sort by state name
    summary.sort(key=lambda x: x["state"])

    return summary

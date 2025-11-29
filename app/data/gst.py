"""GST rates and classification logic for cars in India (September 2025 onwards)."""

from typing import Literal, TypedDict, Optional

FuelType = Literal["Petrol", "Diesel", "CNG", "Electric", "Hybrid"]
GSTCategory = Literal["small", "large", "electric"]


class GSTInfo(TypedDict):
    """GST classification information."""
    category: GSTCategory
    category_name: str
    rate: float
    rate_percent: str
    reason: str
    meets_engine_criteria: Optional[bool]
    meets_length_criteria: Optional[bool]


# GST rates effective September 22, 2025 (GST Reform 2.0)
# Compensation cess abolished
GST_RATES = {
    "small": 0.18,      # 18% for small cars
    "large": 0.40,      # 40% for large cars, SUVs, luxury
    "electric": 0.05,   # 5% for all EVs
}

# Small car thresholds
SMALL_CAR_THRESHOLDS = {
    "Petrol": {"max_engine_cc": 1200, "max_length_mm": 4000},
    "Diesel": {"max_engine_cc": 1500, "max_length_mm": 4000},
    "CNG": {"max_engine_cc": 1200, "max_length_mm": 4000},  # Same as petrol
    "Hybrid": {"max_engine_cc": 1500, "max_length_mm": 4000},  # Uses diesel threshold (higher)
    "Electric": {"max_engine_cc": None, "max_length_mm": None},  # Always 5%
}

# Category display names
CATEGORY_NAMES = {
    "small": "Small Car (18% GST)",
    "large": "Large Car/SUV/Luxury (40% GST)",
    "electric": "Electric Vehicle (5% GST)",
}


def classify_gst_category(
    fuel_type: str,
    engine_cc: Optional[int] = None,
    length_mm: Optional[int] = None,
) -> GSTInfo:
    """
    Classify a car's GST category based on fuel type, engine CC, and length.

    Args:
        fuel_type: Fuel type of the car
        engine_cc: Engine capacity in CC (optional for EVs)
        length_mm: Vehicle length in mm (optional for EVs)

    Returns:
        GSTInfo with category, rate, and explanation
    """
    # Electric vehicles always get 5%
    if fuel_type == "Electric":
        return GSTInfo(
            category="electric",
            category_name=CATEGORY_NAMES["electric"],
            rate=GST_RATES["electric"],
            rate_percent="5%",
            reason="Electric vehicles are charged concessional 5% GST to promote EV adoption",
            meets_engine_criteria=None,
            meets_length_criteria=None,
        )

    thresholds = SMALL_CAR_THRESHOLDS.get(fuel_type, SMALL_CAR_THRESHOLDS["Petrol"])
    max_engine = thresholds["max_engine_cc"]
    max_length = thresholds["max_length_mm"]

    # If no engine/length provided, we can't classify accurately
    if engine_cc is None or length_mm is None:
        # Default to large car assumption for safety (higher tax estimate)
        return GSTInfo(
            category="large",
            category_name=CATEGORY_NAMES["large"],
            rate=GST_RATES["large"],
            rate_percent="40%",
            reason=f"Classification requires engine CC and length. Defaulting to 40% (provide specs for accurate rate)",
            meets_engine_criteria=None,
            meets_length_criteria=None,
        )

    # Check if meets small car criteria (BOTH conditions must be met)
    meets_engine = engine_cc <= max_engine
    meets_length = length_mm <= max_length
    is_small_car = meets_engine and meets_length

    if is_small_car:
        fuel_label = "Petrol/CNG/LPG" if fuel_type in ["Petrol", "CNG"] else fuel_type
        return GSTInfo(
            category="small",
            category_name=CATEGORY_NAMES["small"],
            rate=GST_RATES["small"],
            rate_percent="18%",
            reason=f"Qualifies as small car: {fuel_label} ≤{max_engine}cc AND length ≤{max_length}mm",
            meets_engine_criteria=meets_engine,
            meets_length_criteria=meets_length,
        )
    else:
        # Determine why it doesn't qualify
        reasons = []
        if not meets_engine:
            reasons.append(f"engine {engine_cc}cc > {max_engine}cc limit")
        if not meets_length:
            reasons.append(f"length {length_mm}mm > {max_length}mm limit")

        return GSTInfo(
            category="large",
            category_name=CATEGORY_NAMES["large"],
            rate=GST_RATES["large"],
            rate_percent="40%",
            reason=f"Exceeds small car threshold: {' and '.join(reasons)}",
            meets_engine_criteria=meets_engine,
            meets_length_criteria=meets_length,
        )


def calculate_gst_component(ex_showroom: float, gst_rate: float) -> dict:
    """
    Calculate the GST component embedded in ex-showroom price.

    Ex-showroom price = Base Price + GST
    Base Price = Ex-showroom / (1 + GST rate)
    GST Amount = Ex-showroom - Base Price

    Args:
        ex_showroom: Ex-showroom price (includes GST)
        gst_rate: GST rate as decimal (e.g., 0.18 for 18%)

    Returns:
        Dict with base_price, gst_amount, gst_rate
    """
    base_price = ex_showroom / (1 + gst_rate)
    gst_amount = ex_showroom - base_price

    return {
        "base_price": base_price,
        "gst_amount": gst_amount,
        "gst_rate": gst_rate,
        "gst_percent": f"{gst_rate * 100:.0f}%",
    }


def get_gst_rates_table() -> list[dict]:
    """
    Get GST rates table for display.

    Returns list of dicts with category info.
    """
    return [
        {
            "category": "Small Petrol/CNG/LPG",
            "criteria": "Engine ≤1200cc AND Length ≤4000mm",
            "rate": "18%",
            "previous_rate": "28% + 1% cess = 29%",
        },
        {
            "category": "Small Diesel",
            "criteria": "Engine ≤1500cc AND Length ≤4000mm",
            "rate": "18%",
            "previous_rate": "28% + 3% cess = 31%",
        },
        {
            "category": "Small Hybrid (Petrol)",
            "criteria": "Engine ≤1200cc AND Length ≤4000mm",
            "rate": "18%",
            "previous_rate": "28% + 1% cess = 29%",
        },
        {
            "category": "Small Hybrid (Diesel)",
            "criteria": "Engine ≤1500cc AND Length ≤4000mm",
            "rate": "18%",
            "previous_rate": "28% + 3% cess = 31%",
        },
        {
            "category": "Large Cars / Mid-size",
            "criteria": "Exceeds small car thresholds",
            "rate": "40%",
            "previous_rate": "28% + 17% cess = 45%",
        },
        {
            "category": "SUVs",
            "criteria": "Exceeds small car thresholds",
            "rate": "40%",
            "previous_rate": "28% + 22% cess = 50%",
        },
        {
            "category": "Luxury Cars",
            "criteria": "All luxury vehicles",
            "rate": "40%",
            "previous_rate": "28% + 22% cess = 50%",
        },
        {
            "category": "Electric Vehicles",
            "criteria": "All EVs (any size)",
            "rate": "5%",
            "previous_rate": "5% (unchanged)",
        },
    ]


def get_gst_impact_summary() -> list[dict]:
    """
    Get GST reform impact summary for display.

    Returns list of dicts with before/after comparison.
    """
    return [
        {
            "car_type": "Small Hatchback (e.g., Alto, i10)",
            "old_rate": "29%",
            "new_rate": "18%",
            "savings": "~10% cheaper",
        },
        {
            "car_type": "Compact SUV (e.g., Brezza, Venue)",
            "old_rate": "29-31%",
            "new_rate": "18%",
            "savings": "~10-12% cheaper",
        },
        {
            "car_type": "Mid-size Sedan (e.g., City, Verna)",
            "old_rate": "45%",
            "new_rate": "40%",
            "savings": "~5% cheaper",
        },
        {
            "car_type": "SUV (e.g., Creta, Seltos)",
            "old_rate": "50%",
            "new_rate": "40%",
            "savings": "~10% cheaper",
        },
        {
            "car_type": "Luxury Car (e.g., BMW, Mercedes)",
            "old_rate": "50%",
            "new_rate": "40%",
            "savings": "~10% cheaper",
        },
        {
            "car_type": "Electric Vehicle",
            "old_rate": "5%",
            "new_rate": "5%",
            "savings": "No change (already lowest)",
        },
    ]

"""Brand multipliers for depreciation calculation."""

BRAND_MULTIPLIERS: dict[str, float] = {
    # Slower depreciation (hold value better)
    "Maruti Suzuki": 0.85,
    "Toyota": 0.85,
    "Honda": 0.95,

    # Baseline depreciation
    "Hyundai": 1.0,
    "Kia": 1.0,
    "Tata": 1.0,
    "Mahindra": 1.0,
    "Renault": 1.0,
    "Nissan": 1.0,
    "Ford": 1.0,
    "Citroen": 1.0,

    # Faster depreciation
    "MG": 1.10,
    "Jeep": 1.10,
    "Skoda": 1.15,
    "Volkswagen": 1.15,

    # Luxury (fastest depreciation)
    "BMW": 1.25,
    "Mercedes-Benz": 1.25,
    "Audi": 1.25,
    "Volvo": 1.20,
    "Jaguar": 1.25,
    "Land Rover": 1.25,
    "Porsche": 1.15,
    "Lexus": 1.10,
    "Mini": 1.20,

    # Generic/Other
    "Other": 1.0,
}

# Sorted list for dropdown
BRAND_LIST = sorted([b for b in BRAND_MULTIPLIERS.keys() if b != "Other"]) + ["Other"]


def get_brand_multiplier(brand: str) -> float:
    """Get depreciation multiplier for a brand."""
    return BRAND_MULTIPLIERS.get(brand, 1.0)


def is_luxury_brand(brand: str) -> bool:
    """Check if brand is considered luxury."""
    luxury_brands = {
        "BMW", "Mercedes-Benz", "Audi", "Volvo", "Jaguar",
        "Land Rover", "Porsche", "Lexus", "Mini"
    }
    return brand in luxury_brands

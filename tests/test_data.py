"""Tests for data modules."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.data.road_tax import (
    ROAD_TAX_RATES,
    get_road_tax_rate,
    get_price_category,
    is_ncr_state,
)
from app.data.brands import (
    BRAND_MULTIPLIERS,
    get_brand_multiplier,
    is_luxury_brand,
)
from app.data.constants import (
    STATES,
    FUEL_TYPES,
    OWNER_OPTIONS,
    OWNERSHIP_PREMIUM,
    YEARS,
)


class TestRoadTax:
    """Tests for road tax data."""

    def test_all_states_have_rates(self):
        for state in STATES:
            assert state in ROAD_TAX_RATES or state in ["Chandigarh"]  # May use default

    def test_all_fuel_types_covered(self):
        for state_rates in ROAD_TAX_RATES.values():
            for fuel_type in FUEL_TYPES:
                assert fuel_type in state_rates

    def test_price_category_budget(self):
        assert get_price_category(500000) == "budget"
        assert get_price_category(999999) == "budget"

    def test_price_category_mid(self):
        assert get_price_category(1000000) == "mid"
        assert get_price_category(1999999) == "mid"

    def test_price_category_premium(self):
        assert get_price_category(2000000) == "premium"
        assert get_price_category(5000000) == "premium"

    def test_ncr_states(self):
        assert is_ncr_state("Delhi")
        assert is_ncr_state("Haryana")
        assert is_ncr_state("Uttar Pradesh")
        assert not is_ncr_state("Maharashtra")
        assert not is_ncr_state("Karnataka")

    def test_road_tax_rate_returns_float(self):
        rate = get_road_tax_rate("Delhi", "Petrol", 1500000)
        assert isinstance(rate, float)
        assert 0 < rate < 1


class TestBrands:
    """Tests for brand data."""

    def test_all_brands_have_multipliers(self):
        for brand in BRAND_MULTIPLIERS:
            assert isinstance(BRAND_MULTIPLIERS[brand], float)
            assert BRAND_MULTIPLIERS[brand] > 0

    def test_maruti_holds_value(self):
        assert get_brand_multiplier("Maruti Suzuki") < 1.0

    def test_toyota_holds_value(self):
        assert get_brand_multiplier("Toyota") < 1.0

    def test_luxury_depreciates_faster(self):
        assert get_brand_multiplier("BMW") > 1.0
        assert get_brand_multiplier("Mercedes-Benz") > 1.0
        assert get_brand_multiplier("Audi") > 1.0

    def test_is_luxury_brand(self):
        assert is_luxury_brand("BMW")
        assert is_luxury_brand("Mercedes-Benz")
        assert not is_luxury_brand("Maruti Suzuki")
        assert not is_luxury_brand("Hyundai")

    def test_unknown_brand_returns_baseline(self):
        assert get_brand_multiplier("Unknown Brand XYZ") == 1.0


class TestConstants:
    """Tests for constants."""

    def test_states_not_empty(self):
        assert len(STATES) > 0

    def test_fuel_types_complete(self):
        assert "Petrol" in FUEL_TYPES
        assert "Diesel" in FUEL_TYPES
        assert "Electric" in FUEL_TYPES
        assert "CNG" in FUEL_TYPES
        assert "Hybrid" in FUEL_TYPES

    def test_owner_options(self):
        assert len(OWNER_OPTIONS) == 4
        assert "1st Owner" in OWNER_OPTIONS
        assert "4th+ Owner" in OWNER_OPTIONS

    def test_ownership_premium_increases(self):
        assert OWNERSHIP_PREMIUM[1] < OWNERSHIP_PREMIUM[2]
        assert OWNERSHIP_PREMIUM[2] < OWNERSHIP_PREMIUM[3]
        assert OWNERSHIP_PREMIUM[3] < OWNERSHIP_PREMIUM[4]

    def test_years_range(self):
        assert len(YEARS) == 16  # Last 15 years + current
        assert YEARS[0] > YEARS[-1]  # Descending order

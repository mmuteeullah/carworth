"""Tests for calculator modules."""

import pytest
import sys
from pathlib import Path

# Add app to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.calculators.on_road_price import (
    calculate_on_road_price,
    calculate_road_tax,
    get_insurance_category,
)
from app.calculators.depreciation import (
    calculate_total_depreciation,
    calculate_life_depreciation,
    calculate_ownership_premium,
    calculate_mileage_adjustment,
    get_owner_number,
)
from app.calculators.fair_value import (
    calculate_fair_value,
    calculate_fair_value_range,
    calculate_complete_fair_value,
)
from app.calculators.verdict import (
    get_verdict,
    calculate_difference_percent,
    get_negotiation_target,
)


class TestOnRoadPrice:
    """Tests for on-road price calculations."""

    def test_insurance_category_hatchback(self):
        assert get_insurance_category(800000) == "hatchback"

    def test_insurance_category_sedan(self):
        assert get_insurance_category(1200000) == "sedan"

    def test_insurance_category_suv(self):
        assert get_insurance_category(2000000) == "suv"

    def test_insurance_category_luxury(self):
        assert get_insurance_category(3000000) == "luxury"

    def test_road_tax_delhi_petrol(self):
        tax = calculate_road_tax(1500000, "Delhi", "Petrol")
        assert tax > 0
        assert tax == 1500000 * 0.085  # Mid-range petrol in Delhi

    def test_road_tax_maharashtra_diesel(self):
        tax = calculate_road_tax(1500000, "Maharashtra", "Diesel")
        assert tax == 1500000 * 0.14  # Mid-range diesel in MH

    def test_on_road_price_components(self):
        result = calculate_on_road_price(
            ex_showroom=1500000,
            state="Delhi",
            fuel_type="Petrol",
        )

        assert "ex_showroom" in result
        assert "road_tax" in result
        assert "insurance" in result
        assert "fixed_charges" in result
        assert "on_road_price" in result
        assert result["on_road_price"] > result["ex_showroom"]


class TestDepreciation:
    """Tests for depreciation calculations."""

    def test_owner_number_parsing(self):
        assert get_owner_number("1st Owner") == 1
        assert get_owner_number("2nd Owner") == 2
        assert get_owner_number("3rd Owner") == 3
        assert get_owner_number("4th+ Owner") == 4

    def test_ownership_premium(self):
        assert calculate_ownership_premium(1) == 0.10
        assert calculate_ownership_premium(2) == 0.15
        assert calculate_ownership_premium(3) == 0.20
        assert calculate_ownership_premium(4) == 0.30

    def test_life_depreciation_standard(self):
        dep, age = calculate_life_depreciation(2020, "Petrol", "Maharashtra")
        expected_age = 2025 - 2020  # Current year - manufacture year
        assert age == expected_age
        assert dep == expected_age / 15

    def test_life_depreciation_diesel_ncr(self):
        dep, age = calculate_life_depreciation(2020, "Diesel", "Delhi")
        expected_age = 2025 - 2020
        assert age == expected_age
        assert dep == expected_age / 10  # 10-year rule for NCR diesel

    def test_mileage_adjustment_normal(self):
        adj, status = calculate_mileage_adjustment(45000, 3)  # 15k/year expected
        assert adj == 0.0
        assert status == "normal"

    def test_mileage_adjustment_high(self):
        adj, status = calculate_mileage_adjustment(70000, 3)  # Way above expected
        assert adj == 0.05
        assert status == "high"

    def test_mileage_adjustment_very_low(self):
        adj, status = calculate_mileage_adjustment(10000, 5)  # Very low for 5 years
        assert adj == 0.0
        assert status == "very_low"

    def test_total_depreciation_capped(self):
        # Old car with many factors should be capped at 85%
        result = calculate_total_depreciation(
            year=2010,
            fuel_type="Petrol",
            state="Delhi",
            owner="4th+ Owner",
            km=200000,
            brand="BMW",
            transmission="DCT/DSG",
            body_condition="Poor",
            accident_history="Major",
            service_history="Unknown",
            commercial_use=True,
            new_gen_available=True,
        )

        assert result["total_capped"] == 0.85
        assert result["is_capped"] == True


class TestFairValue:
    """Tests for fair value calculations."""

    def test_basic_fair_value(self):
        value = calculate_fair_value(2000000, 0.40)
        assert value == 1200000  # 60% of 20 lakh

    def test_fair_value_range(self):
        min_val, max_val = calculate_fair_value_range(1000000)
        assert min_val == 950000  # -5%
        assert max_val == 1050000  # +5%

    def test_complete_fair_value_valid_insurance(self):
        result = calculate_complete_fair_value(
            on_road_price=2000000,
            total_depreciation=0.40,
            insurance_valid=True,
            ex_showroom=1500000,
        )

        assert result["insurance_deduction"] == 0
        assert result["fair_value"] == 1200000

    def test_complete_fair_value_expired_insurance(self):
        result = calculate_complete_fair_value(
            on_road_price=2000000,
            total_depreciation=0.40,
            insurance_valid=False,
            ex_showroom=1500000,
        )

        assert result["insurance_deduction"] > 0
        assert result["fair_value"] < 1200000


class TestVerdict:
    """Tests for verdict calculations."""

    def test_difference_percent(self):
        diff = calculate_difference_percent(1100000, 1000000)
        assert diff == 0.10  # 10% overpriced

    def test_verdict_great_deal(self):
        result = get_verdict(asking_price=850000, fair_value=1000000)
        assert result["verdict"] == "Great Deal"
        assert result["color"] == "success"

    def test_verdict_good_deal(self):
        result = get_verdict(asking_price=950000, fair_value=1000000)
        assert result["verdict"] == "Good Deal"
        assert result["color"] == "success"

    def test_verdict_fair_price(self):
        result = get_verdict(asking_price=1050000, fair_value=1000000)
        assert result["verdict"] == "Fair Price"
        assert result["color"] == "warning"

    def test_verdict_slightly_overpriced(self):
        result = get_verdict(asking_price=1120000, fair_value=1000000)
        assert result["verdict"] == "Slightly Overpriced"
        assert result["color"] == "warning"

    def test_verdict_overpriced(self):
        result = get_verdict(asking_price=1200000, fair_value=1000000)
        assert result["verdict"] == "Overpriced"
        assert result["color"] == "error"

    def test_negotiation_target_overpriced(self):
        verdict_result = {"verdict": "Overpriced"}
        target = get_negotiation_target(1000000, verdict_result)
        assert target == 1000000  # Should negotiate to fair value


class TestIntegration:
    """Integration tests with real-world scenarios."""

    def test_honda_city_2022_scenario(self):
        """Test Honda City 2022 calculation (from test cases in spec)."""
        # Ex-showroom 15L, 3 years, 40k km, 1st owner, MH
        on_road = calculate_on_road_price(
            ex_showroom=1500000,
            state="Maharashtra",
            fuel_type="Petrol",
        )

        depreciation = calculate_total_depreciation(
            year=2022,
            fuel_type="Petrol",
            state="Maharashtra",
            owner="1st Owner",
            km=40000,
            brand="Honda",
        )

        fair_value = calculate_complete_fair_value(
            on_road_price=on_road["on_road_price"],
            total_depreciation=depreciation["total_capped"],
            insurance_valid=True,
            ex_showroom=1500000,
        )

        # Should be around 12L as per spec
        assert 1000000 < fair_value["fair_value"] < 1400000

    def test_toyota_fortuner_scenario(self):
        """Test Toyota Fortuner calculation."""
        # Ex-showroom 35L, 4 years, 50k km, 1st owner, DL
        on_road = calculate_on_road_price(
            ex_showroom=3500000,
            state="Delhi",
            fuel_type="Diesel",
        )

        depreciation = calculate_total_depreciation(
            year=2021,
            fuel_type="Diesel",
            state="Delhi",
            owner="1st Owner",
            km=50000,
            brand="Toyota",
        )

        fair_value = calculate_complete_fair_value(
            on_road_price=on_road["on_road_price"],
            total_depreciation=depreciation["total_capped"],
            insurance_valid=True,
            ex_showroom=3500000,
        )

        # Toyota holds value well, should be ~25-27L
        assert 2300000 < fair_value["fair_value"] < 3000000

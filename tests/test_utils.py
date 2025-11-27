"""Tests for utility modules."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.formatters import (
    format_currency,
    format_currency_lakhs,
    format_percentage,
    format_indian_number,
)
from app.utils.validators import (
    validate_ex_showroom,
    validate_km,
    validate_year,
    validate_asking_price,
    validate_inputs,
)


class TestFormatters:
    """Tests for formatting utilities."""

    def test_format_indian_number(self):
        assert format_indian_number(1000) == "1,000"
        assert format_indian_number(10000) == "10,000"
        assert format_indian_number(100000) == "1,00,000"
        assert format_indian_number(1000000) == "10,00,000"
        assert format_indian_number(10000000) == "1,00,00,000"

    def test_format_currency_with_symbol(self):
        result = format_currency(1500000)
        assert "Rs." in result
        assert "15" in result

    def test_format_currency_without_symbol(self):
        result = format_currency(1500000, include_symbol=False)
        assert "Rs." not in result

    def test_format_currency_lakhs(self):
        assert format_currency_lakhs(1500000) == "15.00 L"
        assert format_currency_lakhs(1234567) == "12.35 L"
        assert format_currency_lakhs(100000) == "1.00 L"

    def test_format_percentage(self):
        assert format_percentage(0.125) == "12.5%"
        assert format_percentage(0.5) == "50.0%"
        assert format_percentage(0.333, decimal_places=2) == "33.30%"


class TestValidators:
    """Tests for input validators."""

    def test_validate_ex_showroom_valid(self):
        is_valid, error = validate_ex_showroom(1500000)
        assert is_valid
        assert error is None

    def test_validate_ex_showroom_too_low(self):
        is_valid, error = validate_ex_showroom(50000)
        assert not is_valid
        assert error is not None

    def test_validate_ex_showroom_too_high(self):
        is_valid, error = validate_ex_showroom(100000000)
        assert not is_valid
        assert error is not None

    def test_validate_km_valid(self):
        is_valid, error = validate_km(50000)
        assert is_valid
        assert error is None

    def test_validate_km_negative(self):
        is_valid, error = validate_km(-1000)
        assert not is_valid
        assert error is not None

    def test_validate_km_too_high(self):
        is_valid, error = validate_km(600000)
        assert not is_valid
        assert error is not None

    def test_validate_year_valid(self):
        is_valid, error = validate_year(2022)
        assert is_valid
        assert error is None

    def test_validate_year_future(self):
        is_valid, error = validate_year(2030)
        assert not is_valid
        assert error is not None

    def test_validate_year_too_old(self):
        is_valid, error = validate_year(1990)
        assert not is_valid
        assert error is not None

    def test_validate_inputs_all_valid(self):
        inputs = {
            "ex_showroom": 1500000,
            "km": 50000,
            "year": 2022,
            "asking_price": 1000000,
        }
        is_valid, errors = validate_inputs(inputs)
        assert is_valid
        assert len(errors) == 0

    def test_validate_inputs_multiple_errors(self):
        inputs = {
            "ex_showroom": 50000,  # Invalid
            "km": -1000,  # Invalid
            "year": 2030,  # Invalid
            "asking_price": 1000000,
        }
        is_valid, errors = validate_inputs(inputs)
        assert not is_valid
        assert len(errors) >= 3

"""Input validation utilities."""

from typing import Optional
from app.data.constants import CURRENT_YEAR


def validate_ex_showroom(value: float) -> tuple[bool, Optional[str]]:
    """
    Validate ex-showroom price.

    Returns:
        tuple: (is_valid, error_message)
    """
    if value < 100000:
        return False, "Ex-showroom price must be at least Rs. 1,00,000"
    if value > 50000000:
        return False, "Ex-showroom price cannot exceed Rs. 5 crore"
    return True, None


def validate_km(value: int) -> tuple[bool, Optional[str]]:
    """
    Validate kilometers driven.

    Returns:
        tuple: (is_valid, error_message)
    """
    if value < 0:
        return False, "Kilometers cannot be negative"
    if value > 500000:
        return False, "Kilometers seem unusually high (max 5,00,000)"
    return True, None


def validate_year(value: int) -> tuple[bool, Optional[str]]:
    """
    Validate manufacturing year.

    Returns:
        tuple: (is_valid, error_message)
    """
    if value > CURRENT_YEAR:
        return False, "Year cannot be in the future"
    if value < CURRENT_YEAR - 20:
        return False, "Car is too old (max 20 years)"
    return True, None


def validate_asking_price(value: float) -> tuple[bool, Optional[str]]:
    """
    Validate asking price.

    Returns:
        tuple: (is_valid, error_message)
    """
    if value < 50000:
        return False, "Asking price must be at least Rs. 50,000"
    if value > 50000000:
        return False, "Asking price cannot exceed Rs. 5 crore"
    return True, None


def validate_inputs(inputs: dict) -> tuple[bool, list[str]]:
    """
    Validate all inputs.

    Returns:
        tuple: (all_valid, list_of_errors)
    """
    errors = []

    # Validate ex-showroom
    valid, error = validate_ex_showroom(inputs.get("ex_showroom", 0))
    if not valid:
        errors.append(error)

    # Validate km
    valid, error = validate_km(inputs.get("km", 0))
    if not valid:
        errors.append(error)

    # Validate year
    valid, error = validate_year(inputs.get("year", CURRENT_YEAR))
    if not valid:
        errors.append(error)

    # Validate asking price
    valid, error = validate_asking_price(inputs.get("asking_price", 0))
    if not valid:
        errors.append(error)

    return len(errors) == 0, errors

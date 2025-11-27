"""Formatting utilities for currency and numbers."""

import locale

# Set locale for Indian number formatting
try:
    locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'en_IN')
    except locale.Error:
        pass  # Fall back to default


def format_currency(amount: float, include_symbol: bool = True) -> str:
    """
    Format amount as Indian currency.

    Examples:
        1500000 -> "Rs. 15,00,000"
        1234567 -> "Rs. 12,34,567"
    """
    try:
        formatted = locale.format_string('%d', int(amount), grouping=True)
    except (ValueError, locale.Error):
        formatted = format_indian_number(int(amount))

    if include_symbol:
        return f"Rs. {formatted}"
    return formatted


def format_indian_number(num: int) -> str:
    """Format number with Indian comma notation (lakhs, crores)."""
    s = str(num)
    if len(s) <= 3:
        return s

    # Last 3 digits
    result = s[-3:]
    s = s[:-3]

    # Rest in groups of 2
    while s:
        result = s[-2:] + ',' + result
        s = s[:-2]

    return result


def format_currency_lakhs(amount: float, decimal_places: int = 2) -> str:
    """
    Format amount in lakhs with specified decimal places.

    Examples:
        1500000 -> "15.00 L"
        1234567 -> "12.35 L"
    """
    lakhs = amount / 100000
    return f"{lakhs:,.{decimal_places}f} L"


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """
    Format decimal as percentage.

    Examples:
        0.125 -> "12.5%"
        0.3333 -> "33.3%"
    """
    return f"{value * 100:.{decimal_places}f}%"


def format_number(value: float, decimal_places: int = 0) -> str:
    """Format number with commas."""
    if decimal_places == 0:
        return format_indian_number(int(value))
    return f"{value:,.{decimal_places}f}"


def format_km(km: int) -> str:
    """Format kilometers driven."""
    return f"{format_indian_number(km)} km"


def format_age(years: int) -> str:
    """Format car age."""
    if years == 1:
        return "1 year"
    return f"{years} years"

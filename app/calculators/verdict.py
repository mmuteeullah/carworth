"""Verdict engine for deal assessment."""

from app.data.constants import VERDICT_THRESHOLDS
from app.data.road_tax import is_ncr_state


def calculate_difference_percent(asking_price: float, fair_value: float) -> float:
    """Calculate percentage difference between asking and fair value."""
    if fair_value == 0:
        return 0.0
    return (asking_price - fair_value) / fair_value


def get_verdict(asking_price: float, fair_value: float) -> dict:
    """
    Determine verdict based on asking price vs fair value.

    Returns dict with:
    - verdict: Text verdict
    - emoji: Verdict emoji
    - color: CSS color for display
    - difference_percent: Percentage difference
    - difference_amount: Absolute difference
    """
    diff_percent = calculate_difference_percent(asking_price, fair_value)
    diff_amount = asking_price - fair_value

    if diff_percent <= VERDICT_THRESHOLDS["great_deal"]:
        verdict = "Great Deal"
        emoji = "check-circle"
        color = "success"
    elif diff_percent <= VERDICT_THRESHOLDS["good_deal"]:
        verdict = "Good Deal"
        emoji = "check"
        color = "success"
    elif diff_percent <= VERDICT_THRESHOLDS["fair"]:
        verdict = "Fair Price"
        emoji = "minus"
        color = "warning"
    elif diff_percent <= VERDICT_THRESHOLDS["slightly_overpriced"]:
        verdict = "Slightly Overpriced"
        emoji = "alert-triangle"
        color = "warning"
    else:
        verdict = "Overpriced"
        emoji = "x-circle"
        color = "error"

    return {
        "verdict": verdict,
        "emoji": emoji,
        "color": color,
        "difference_percent": diff_percent,
        "difference_amount": diff_amount,
    }


def get_negotiation_target(fair_value: float, verdict_result: dict) -> float:
    """
    Calculate suggested negotiation target price.

    For overpriced cars, suggest negotiating to fair value.
    For fair/good deals, suggest negotiating 3-5% lower.
    """
    verdict = verdict_result["verdict"]

    if verdict in ["Overpriced", "Slightly Overpriced"]:
        return fair_value  # Negotiate to fair value
    elif verdict == "Fair Price":
        return fair_value * 0.97  # Try for 3% below fair
    else:
        return fair_value * 0.95  # Try for 5% below fair


def generate_warnings(
    fuel_type: str,
    state: str,
    age: int,
    mileage_status: str,
    owner: str,
    accident_history: str,
    commercial_use: bool,
    transmission: str,
) -> list[dict]:
    """
    Generate warning messages for edge cases.

    Returns list of warning dicts with:
    - type: warning/info/danger
    - title: Short title
    - message: Detailed message
    """
    warnings = []

    # Diesel NCR warning
    if fuel_type == "Diesel" and is_ncr_state(state):
        remaining_years = 10 - age
        if remaining_years <= 3:
            warnings.append({
                "type": "danger",
                "title": "Diesel NCR Restriction",
                "message": f"Only {remaining_years} years remaining for registration in NCR. "
                           f"10-year diesel ban applies. Resale will be very difficult.",
            })
        elif remaining_years <= 5:
            warnings.append({
                "type": "warning",
                "title": "Diesel NCR Alert",
                "message": f"Only {remaining_years} years remaining. Consider this for resale.",
            })

    # Very low mileage warning
    if mileage_status == "very_low":
        warnings.append({
            "type": "warning",
            "title": "Very Low Mileage",
            "message": "Mileage is unusually low. Could indicate odometer tampering or "
                       "long stationary periods causing mechanical issues. Verify carefully.",
        })

    # High mileage warning
    if mileage_status == "high":
        warnings.append({
            "type": "info",
            "title": "High Mileage",
            "message": "Mileage is above average. Ensure thorough mechanical inspection.",
        })

    # Multiple owner warning
    if owner in ["3rd Owner", "4th+ Owner"]:
        warnings.append({
            "type": "warning",
            "title": "Multiple Owners",
            "message": "Multiple previous owners increase risk of undisclosed issues. "
                       "Verify complete service history.",
        })

    # Accident history warning
    if accident_history == "Major":
        warnings.append({
            "type": "danger",
            "title": "Major Accident History",
            "message": "Car has major accident history. Structural integrity may be "
                       "compromised. Get professional inspection.",
        })
    elif accident_history == "Minor":
        warnings.append({
            "type": "warning",
            "title": "Minor Accident History",
            "message": "Minor accident reported. Check for quality of repairs.",
        })

    # Commercial use warning
    if commercial_use:
        warnings.append({
            "type": "warning",
            "title": "Commercial Use",
            "message": "Car was used commercially. Expect higher wear and tear.",
        })

    # DCT/DSG warning
    if transmission == "DCT/DSG":
        warnings.append({
            "type": "info",
            "title": "DCT/DSG Transmission",
            "message": "Dual-clutch transmissions can have expensive repairs. "
                       "Check for shuddering or jerky shifts during test drive.",
        })

    # Old car warning
    if age >= 10:
        warnings.append({
            "type": "warning",
            "title": "Older Vehicle",
            "message": f"Car is {age} years old. Ensure parts availability and "
                       f"consider maintenance costs.",
        })

    return warnings


def get_checklist() -> list[dict]:
    """Return due diligence checklist items."""
    return [
        {
            "category": "Documents",
            "items": [
                "Verify RC (Registration Certificate) is original",
                "Check for hypothecation - ensure NOC if loan was taken",
                "Verify insurance policy and claim history",
                "Check for challan/pending fines",
                "Verify PUC (Pollution Under Control) certificate",
            ],
        },
        {
            "category": "Physical Inspection",
            "items": [
                "Check body panels for dents, scratches, repaint",
                "Look for uneven panel gaps (accident indicator)",
                "Check tyre condition and brand consistency",
                "Inspect under the car for rust/oil leaks",
                "Check interior wear - seats, steering, pedals",
            ],
        },
        {
            "category": "Mechanical",
            "items": [
                "Cold start the engine",
                "Check for unusual sounds or vibrations",
                "Test all gears and clutch/brake feel",
                "Verify AC cooling performance",
                "Test all electrical - windows, locks, lights, infotainment",
            ],
        },
        {
            "category": "Verification",
            "items": [
                "Match chassis/engine number with RC",
                "Verify service history at authorized dealer",
                "Run vehicle history check (Vahaan portal)",
                "Confirm current owner matches RC",
                "Take extended test drive in various conditions",
            ],
        },
    ]

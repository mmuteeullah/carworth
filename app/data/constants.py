"""Constants and fixed values for calculations."""

from datetime import datetime

# Current year for age calculation
CURRENT_YEAR = datetime.now().year

# Fixed charges (in INR) - Updated based on actual dealer data Nov 2025
FIXED_CHARGES = {
    "registration": 4000,      # Registration fee (varies by state, avg)
    "hsrp": 1100,              # High Security Registration Plate
    "hypothecation": 1500,     # Only if loan
    "fastag": 600,             # Mandatory FasTag
    "rto_misc": 2000,          # RTO miscellaneous (forms, smart card, etc.)
}

# Handling/Logistics charges by price category (dealer charges)
# These are typically non-negotiable and included in on-road price
HANDLING_CHARGES = {
    "budget": 15000,       # < 8 lakh
    "compact": 18000,      # 8-12 lakh
    "mid": 22000,          # 12-18 lakh
    "premium": 25000,      # 18-30 lakh
    "luxury": 35000,       # > 30 lakh
}

# TCS (Tax Collected at Source) - 1% on ex-showroom if > 10 lakh
TCS_THRESHOLD = 1000000  # 10 lakh
TCS_RATE = 0.01  # 1%

# Insurance estimates by price category (in INR) - Updated Nov 2025
# Based on comprehensive 1-year insurance with zero depreciation
INSURANCE_ESTIMATES = {
    "budget": 28000,       # < 6 lakh (hatchbacks like Alto, Swift)
    "hatchback": 35000,    # 6-10 lakh (i20, Baleno, Punch)
    "compact_suv": 45000,  # 10-14 lakh (Nexon, Venue, Sonet)
    "sedan": 55000,        # 14-18 lakh (City, Verna, Creta)
    "suv": 70000,          # 18-25 lakh (Seltos, Harrier)
    "premium_suv": 85000,  # 25-40 lakh (Fortuner, XUV700)
    "luxury": 110000,      # > 40 lakh
}

# Ownership premium (added to depreciation)
OWNERSHIP_PREMIUM = {
    1: 0.10,   # 1st owner: +10%
    2: 0.15,   # 2nd owner: +15%
    3: 0.20,   # 3rd owner: +20%
    4: 0.30,   # 4th+ owner: +30%
}

# Transmission adjustment (added to depreciation)
TRANSMISSION_ADJUSTMENT = {
    "Manual": 0.0,
    "CVT": 0.0,
    "Torque Converter": 0.0,
    "AMT": 0.02,
    "DCT/DSG": 0.05,
}

# Condition adjustments
CONDITION_ADJUSTMENTS = {
    "body": {
        "Excellent": -0.02,
        "Good": 0.0,
        "Average": 0.02,
        "Poor": 0.05,
    },
    "accident": {
        "None": 0.0,
        "Minor": 0.10,
        "Major": 0.20,
    },
    "service": {
        "Full Authorized": -0.02,
        "Partial": 0.0,
        "Unknown": 0.03,
    },
    "commercial": 0.15,       # If used commercially
    "new_gen_available": 0.05,  # If new generation is available
}

# Life expectancy for depreciation calculation
CAR_LIFE_YEARS = 15
DIESEL_NCR_LIFE_YEARS = 10

# Maximum depreciation cap
MAX_DEPRECIATION = 0.85

# Expected annual mileage
EXPECTED_ANNUAL_KM = 15000

# Mileage thresholds for adjustment
MILEAGE_THRESHOLDS = {
    "high": 1.3,      # > 30% above expected
    "slight_high": 1.1,  # > 10% above expected
    "very_low": 0.5,  # < 50% of expected
}

MILEAGE_ADJUSTMENTS = {
    "high": 0.05,
    "slight_high": 0.02,
}

# Fair value range percentage
FAIR_VALUE_RANGE = 0.05  # +/- 5%

# Verdict thresholds
VERDICT_THRESHOLDS = {
    "great_deal": -0.10,   # <= -10%
    "good_deal": 0.0,      # <= 0%
    "fair": 0.07,          # <= 7%
    "slightly_overpriced": 0.15,  # <= 15%
    # > 15% is overpriced
}

# Dropdown options
STATES = [
    "Delhi", "Haryana", "Maharashtra", "Karnataka", "Telangana",
    "Tamil Nadu", "Uttar Pradesh", "Gujarat", "Rajasthan", "Punjab",
    "West Bengal", "Kerala", "Madhya Pradesh", "Bihar", "Odisha",
    "Andhra Pradesh", "Jharkhand", "Chhattisgarh", "Uttarakhand",
    "Himachal Pradesh", "Assam", "Goa", "Chandigarh"
]

FUEL_TYPES = ["Petrol", "Diesel", "CNG", "Electric", "Hybrid"]

OWNER_OPTIONS = ["1st Owner", "2nd Owner", "3rd Owner", "4th+ Owner"]

BRAND_OPTIONS = [
    "Maruti Suzuki", "Toyota", "Honda", "Hyundai", "Kia", "Tata",
    "Mahindra", "MG", "Skoda", "Volkswagen", "Jeep", "Renault",
    "Nissan", "Ford", "BMW", "Mercedes-Benz", "Audi", "Volvo",
    "Jaguar", "Land Rover", "Porsche", "Lexus", "Mini", "Citroen", "Other"
]

TRANSMISSION_OPTIONS = ["Manual", "CVT", "Torque Converter", "AMT", "DCT/DSG"]

CONDITION_OPTIONS = ["Excellent", "Good", "Average", "Poor"]

ACCIDENT_OPTIONS = ["None", "Minor", "Major"]

SERVICE_OPTIONS = ["Full Authorized", "Partial", "Unknown"]

INSURANCE_OPTIONS = ["Valid", "Expired"]

# Year options (last 15 years)
YEARS = list(range(CURRENT_YEAR, CURRENT_YEAR - 16, -1))

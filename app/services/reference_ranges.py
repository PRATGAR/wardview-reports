RANGES = {
    "glucose": {"unit": "mmol/L", "low": 3.9, "high": 5.6, "critical_low": 2.8, "critical_high": 22.2},
    "hemoglobin": {"unit": "g/dL", "low": 12.0, "high": 17.5, "critical_low": 7.0, "critical_high": 20.0},
    "potassium": {"unit": "mmol/L", "low": 3.5, "high": 5.1, "critical_low": 2.5, "critical_high": 6.5},
    "sodium": {"unit": "mmol/L", "low": 135.0, "high": 145.0, "critical_low": 120.0, "critical_high": 160.0},
    "creatinine": {"unit": "umol/L", "low": 45.0, "high": 110.0, "critical_low": None, "critical_high": 600.0},
    "crp": {"unit": "mg/L", "low": 0.0, "high": 5.0, "critical_low": None, "critical_high": 200.0},
    "wbc": {"unit": "10^9/L", "low": 4.0, "high": 11.0, "critical_low": 2.0, "critical_high": 30.0},
}


def normalise_name(analyte):
    return (analyte or "").strip().lower()


def expected_unit(analyte):
    entry = RANGES.get(normalise_name(analyte))
    return entry["unit"] if entry else None


def flag_for(analyte, value):
    entry = RANGES.get(normalise_name(analyte))
    if entry is None or value is None:
        return "N"
    critical_low = entry["critical_low"]
    critical_high = entry["critical_high"]
    if critical_low is not None and value < critical_low:
        return "C"
    if critical_high is not None and value > critical_high:
        return "C"
    if value < entry["low"]:
        return "L"
    if value > entry["high"]:
        return "H"
    return "N"


def summarise_flags(rows):
    counts = {"L": 0, "N": 0, "H": 0, "C": 0}
    for row in rows:
        flag = row["flag"] if row["flag"] in counts else "N"
        counts[flag] += 1
    return counts

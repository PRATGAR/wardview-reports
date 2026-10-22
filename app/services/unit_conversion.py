"""Conversion of instrument units into the units used by the reference table."""

CONVERSIONS = {
    ("glucose", "mg/dl"): ("mmol/L", 0.0555),
    ("creatinine", "mg/dl"): ("umol/L", 88.4),
    ("hemoglobin", "g/l"): ("g/dL", 0.1),
    ("sodium", "meq/l"): ("mmol/L", 1.0),
    ("potassium", "meq/l"): ("mmol/L", 1.0),
    ("crp", "mg/dl"): ("mg/L", 10.0),
}


def _key(analyte, unit):
    return (analyte or "").strip().lower(), (unit or "").strip().lower()


def can_convert(analyte, unit):
    return _key(analyte, unit) in CONVERSIONS


def convert(analyte, value, unit):
    """Return (value, unit) expressed in the reference unit when a rule exists."""
    if value is None:
        return value, unit
    rule = CONVERSIONS.get(_key(analyte, unit))
    if rule is None:
        return value, unit
    target_unit, factor = rule
    return round(value * factor, 3), target_unit


def convert_rows(rows):
    converted = []
    for row in rows:
        value, unit = convert(row["analyte"], row["value"], row["unit"])
        converted.append({**row, "value": value, "unit": unit})
    return converted

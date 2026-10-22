from datetime import date


def age_from_birth(birth_date, today=None):
    today = today or date.today()
    try:
        born = date.fromisoformat(birth_date)
    except (TypeError, ValueError):
        return None
    years = today.year - born.year
    if (today.month, today.day) < (born.month, born.day):
        years -= 1
    return years


def format_value(value, unit):
    if value is None:
        return "n/a"
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return f"{text} {unit}".strip()


def initials(full_name):
    parts = [p for p in (full_name or "").split() if p]
    return "".join(p[0].upper() for p in parts[:2])


def mask_mrn(mrn):
    if not mrn or len(mrn) < 4:
        return mrn
    return "*" * (len(mrn) - 4) + mrn[-4:]


def describe_flag(flag):
    return {
        "L": "below reference range",
        "N": "within reference range",
        "H": "above reference range",
        "C": "critical value",
    }.get(flag, "unclassified")

import re
from datetime import date

SORT_COLUMNS = {
    "name": "p.full_name",
    "mrn": "p.mrn",
    "ward": "p.ward",
    "birth": "p.birth_date",
}
DEFAULT_SORT = "p.full_name"

TEST_CODE_RE = re.compile(r"[A-Z0-9_\-]{2,12}")
ANALYTE_RE = re.compile(r"^[A-Za-z0-9 _\-]{1,40}$")
EXPORT_NAME_STRIP_RE = re.compile(r"[^A-Za-z0-9_.\-]")
TEMPLATE_BLOCK_RE = re.compile(r"\{%.*?%\}", re.DOTALL)
MAX_TEMPLATE_CHARS = 8000


def parse_positive_int(raw, default=None):
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return default
    return value if value > 0 else default


def is_valid_test_code(code):
    return bool(TEST_CODE_RE.match(code or ""))


def validate_criteria(data):
    analyte = (data.get("analyte") or "").strip()
    if analyte and not ANALYTE_RE.match(analyte):
        raise ValueError("analyte contains unsupported characters")
    unit = clean_unit(data.get("unit"))
    return {"analyte": analyte, "unit": unit}


def clean_unit(raw):
    return (raw or "").strip()[:24]


def clean_export_name(raw):
    cleaned = EXPORT_NAME_STRIP_RE.sub("", raw or "")
    cleaned = cleaned.lstrip(".")[:64]
    if not cleaned:
        raise ValueError("export name is empty after cleaning")
    return cleaned


def prepare_template_text(text):
    stripped = TEMPLATE_BLOCK_RE.sub("", text or "")
    if len(stripped) > MAX_TEMPLATE_CHARS:
        raise ValueError("template text is too long")
    return stripped


def is_local_path(target):
    if not target or not target.startswith("/"):
        return False
    if target.startswith("//") or "\\" in target:
        return False
    return True


def is_internal_path(target):
    return bool(target) and target.startswith("/")


def is_allowed_callback(url, prefix):
    return bool(url) and url.startswith(prefix)


def parse_iso_date(raw):
    try:
        return date.fromisoformat(raw)
    except (TypeError, ValueError):
        return None


def like_term(raw):
    return raw.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

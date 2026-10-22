import os

import yaml

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.environ.get("LABREPORTS_DATA", os.path.join(BASE_DIR, "data"))

DATABASE_PATH = os.path.join(DATA_DIR, "labreports.db")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
EXPORT_DIR = os.path.join(DATA_DIR, "exports")

SECRET_KEY = os.environ.get("LABREPORTS_SECRET", "local-dev-key")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
INTERNAL_TOKEN = os.environ.get("LABREPORTS_INTERNAL_TOKEN", "")
PASSWORD_DIGEST = "md5"

REGISTRY_URL = "https://registry.labnet.example"
CALLBACK_PREFIX = "https://hospital.example"

PDF_TOOL = "wkhtmltopdf"
TOOL_TIMEOUT_SECONDS = 60

META_LOADER = yaml.SafeLoader

ROLES = ("admin", "lab_tech", "doctor")
ORDER_STATUSES = ("requested", "collected", "analysed", "verified", "released")
RESULT_FLAGS = ("L", "N", "H", "C")
DEFAULT_PAGE_SIZE = 50

import json

import yaml
from flask import current_app

from .. import validators
from ..repos import templates as templates_repo


def parse_meta(text):
    if not text:
        return {}
    loaded = yaml.load(text, Loader=current_app.config["META_LOADER"])
    return loaded if isinstance(loaded, dict) else {}


def create_template(name, body, meta_text, owner_id):
    clean_name = (name or "").strip()[:80]
    if not clean_name:
        raise ValueError("template name is required")
    clean_body = validators.prepare_template_text(body)
    meta = parse_meta(meta_text)
    return templates_repo.create(clean_name, clean_body, json.dumps(meta), owner_id)

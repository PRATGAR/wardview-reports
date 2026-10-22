import requests
from flask import current_app


def fetch_profile(mrn):
    url = f"{current_app.config['REGISTRY_URL']}/patients/{mrn}"
    response = requests.request("GET", url, timeout=5)
    if not response.ok:
        return None
    return response.json()

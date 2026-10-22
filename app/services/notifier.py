import time

import requests

MAX_ATTEMPTS = 3
REQUEST_TIMEOUT_SECONDS = 5


def _deliver(url, payload):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.request("POST", url, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
            if response.ok:
                return True
        except requests.RequestException:
            pass
        time.sleep(0.5 * attempt)
    return False


def notify_doctor(doctor, report, token):
    url = doctor["callback_url"]
    if not url:
        return False
    payload = {
        "event": "report.shared",
        "report_id": report["id"],
        "title": report["title"],
        "token": token,
    }
    return _deliver(url, payload)

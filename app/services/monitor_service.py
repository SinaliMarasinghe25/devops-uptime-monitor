import time
from urllib.parse import urlparse

import requests


def is_valid_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ["http", "https"] and parsed_url.netloc != ""


def check_website_status(url):
    if not is_valid_url(url):
        return {
            "url": url,
            "status": "INVALID",
            "status_code": None,
            "response_time_ms": None,
            "message": "Please enter a valid URL starting with http:// or https://"
        }

    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        end_time = time.time()

        response_time_ms = round((end_time - start_time) * 1000, 2)

        if 200 <= response.status_code < 400:
            status = "UP"
            message = "Website is reachable"
        else:
            status = "DOWN"
            message = "Website responded with an error status"

        return {
            "url": url,
            "status": status,
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
            "message": message
        }

    except requests.exceptions.Timeout:
        return {
            "url": url,
            "status": "DOWN",
            "status_code": None,
            "response_time_ms": None,
            "message": "Website request timed out"
        }

    except requests.exceptions.RequestException as error:
        return {
            "url": url,
            "status": "DOWN",
            "status_code": None,
            "response_time_ms": None,
            "message": str(error)
        }
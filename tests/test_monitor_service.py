import requests

from app.services.monitor_service import is_valid_url, check_website_status


def test_valid_url_returns_true():
    assert is_valid_url("https://github.com") is True


def test_invalid_url_returns_false():
    assert is_valid_url("github.com") is False


def test_invalid_url_status():
    result = check_website_status("github.com")

    assert result["status"] == "INVALID"
    assert result["status_code"] is None
    assert result["response_time_ms"] is None


def test_successful_website_check(monkeypatch):
    class MockResponse:
        status_code = 200

    def mock_get(url, timeout):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = check_website_status("https://github.com")

    assert result["status"] == "UP"
    assert result["status_code"] == 200
    assert result["response_time_ms"] is not None


def test_timeout_website_check(monkeypatch):
    def mock_get(url, timeout):
        raise requests.exceptions.Timeout

    monkeypatch.setattr(requests, "get", mock_get)

    result = check_website_status("https://slow-website.com")

    assert result["status"] == "DOWN"
    assert result["message"] == "Website request timed out"
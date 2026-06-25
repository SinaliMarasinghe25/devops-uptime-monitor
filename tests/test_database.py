from app.models import MonitoredService, StatusCheck


def test_valid_url_check_is_saved_to_database(client, app, monkeypatch):
    class MockResponse:
        status_code = 200

    def mock_get(url, timeout):
        return MockResponse()

    monkeypatch.setattr(
        "app.services.monitor_service.requests.get",
        mock_get
    )

    response = client.post(
        "/",
        data={"url": "https://github.com"}
    )

    assert response.status_code == 200

    with app.app_context():
        service = MonitoredService.query.filter_by(
            url="https://github.com"
        ).first()

        assert service is not None
        assert service.name == "github.com"

        status_check = StatusCheck.query.filter_by(
            service_id=service.id
        ).first()

        assert status_check is not None
        assert status_check.status == "UP"
        assert status_check.status_code == 200
        assert status_check.response_time_ms is not None


def test_invalid_url_is_not_saved_to_database(client, app):
    response = client.post(
        "/",
        data={"url": "github.com"}
    )

    assert response.status_code == 200

    with app.app_context():
        assert MonitoredService.query.count() == 0
        assert StatusCheck.query.count() == 0


def test_dashboard_shows_recent_checks(client, monkeypatch):
    class MockResponse:
        status_code = 200

    def mock_get(url, timeout):
        return MockResponse()

    monkeypatch.setattr(
        "app.services.monitor_service.requests.get",
        mock_get
    )

    response = client.post(
        "/",
        data={"url": "https://github.com"}
    )

    assert response.status_code == 200
    assert b"Recent Checks" in response.data
    assert b"github.com" in response.data
    assert b"UP" in response.data
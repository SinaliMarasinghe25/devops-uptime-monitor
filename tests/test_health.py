def test_health_endpoint_returns_healthy_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"
    assert response.get_json()["service"] == "DevOps Uptime Monitor"


def test_dashboard_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Uptime Monitor" in response.data
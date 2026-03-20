from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test that the API is running and accessible."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API running"}

def test_get_incidents():
    """Test that the public incidents endpoint returns a list."""
    response = client.get("/incidents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_analytics_hotspots():
    """Test the complex aggregation endpoint."""
    response = client.get("/analytics/hotspots")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Verify the data structure contains our expected keys
    if len(data) > 0:
        assert "location" in data[0]
        assert "total_delay_minutes" in data[0]
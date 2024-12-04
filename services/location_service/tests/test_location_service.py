import pytest
from location_service.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_location_missing_city(client):
    response = client.get('/location')
    assert response.status_code == 404

def test_location_city_not_found(client):
    response = client.get('/location?city=NonexistentCity')
    assert response.status_code == 404
    assert response.json['error'] == "City not found"

def test_location_city_found(client):
    response = client.get('/location?city=New York')
    assert response.status_code == 200
    assert response.json == {"lat": 40.7128, "lon": -74.0060}

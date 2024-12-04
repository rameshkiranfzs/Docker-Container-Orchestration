import pytest
from weather_service.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_weather_missing_coordinates(client):
    response = client.get('/weather')
    assert response.status_code == 400
    assert response.json['error'] == "Latitude and Longitude are required"

def test_weather_success(client, mocker):
    mocker.patch('requests.get', return_value=type('MockResponse', (), {
        'status_code': 200, 
        'json': lambda: {"temp": 15.0, "humidity": 80}
    }))
    response = client.get('/weather?lat=40.7128&lon=-74.0060')
    assert response.status_code == 200
    assert 'temp' in response.json
    assert response.json['temp'] == 15.0

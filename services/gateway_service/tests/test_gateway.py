import pytest
from gateway.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_weather_endpoint_missing_city(client):
    response = client.get('/weather')
    assert response.status_code == 400
    assert response.json['error'] == "City is required"

def test_weather_endpoint_success(client, mocker):
    mocker.patch('requests.get', side_effect=lambda url, params: 
        {'http://location_service:5002/location': 
            type('MockResponse', (), {'status_code': 200, 'json': lambda: {"lat": 40.7128, "lon": -74.0060}}),
         'http://weather_service:5001/weather': 
            type('MockResponse', (), {'status_code': 200, 'json': lambda: {"temp": 15.0, "humidity": 80}})
        }[url]
    )

    response = client.get('/weather?city=New York')
    assert response.status_code == 200
    assert 'temp' in response.json
    assert response.json['temp'] == 15.0

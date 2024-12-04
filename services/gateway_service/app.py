from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

WEATHER_SERVICE_URL = "http://weather_service:5001"
LOCATION_SERVICE_URL = "http://location_service:5002"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City is required"}), 400

    # Resolve city to coordinates
    location_res = requests.get(f"{LOCATION_SERVICE_URL}/location", params={"city": city})
    if location_res.status_code != 200:
        return jsonify({"error": "Failed to resolve location"}), 500

    coordinates = location_res.json()
    weather_res = requests.get(f"{WEATHER_SERVICE_URL}/weather", params=coordinates)
    if weather_res.status_code != 200:
        return jsonify({"error": "Failed to fetch weather"}), 500

    return jsonify(weather_res.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

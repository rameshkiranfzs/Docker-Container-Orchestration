from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPENWEATHER_API_KEY = "your_api_key"  # Replace with your OpenWeather API key
OPENWEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    response = requests.get(OPENWEATHER_URL, params={
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY
    })
    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

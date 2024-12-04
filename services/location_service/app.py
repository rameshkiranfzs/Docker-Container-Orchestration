from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy location resolver for simplicity
LOCATION_DATABASE = {
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Tokyo": {"lat": 35.6895, "lon": 139.6917},
}

@app.route('/location', methods=['GET'])
def get_location():
    city = request.args.get('city')
    if not city or city not in LOCATION_DATABASE:
        return jsonify({"error": "City not found"}), 404
    return jsonify(LOCATION_DATABASE[city])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

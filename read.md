# Real-Time Weather API

## Overview

The **Real-Time Weather API** is a microservices-based architecture designed to provide real-time weather information for a given city. The system consists of three main services: **API Gateway**, **Weather Service**, and **Location Service**. The **API Gateway** handles incoming requests and coordinates data retrieval from the other services, which are responsible for specific tasks such as fetching weather data and resolving city names into geographic coordinates.

This application uses **Flask** as the web framework for each microservice, and Docker is used to containerize the services for easy deployment.

## Architecture

The system follows a **microservices architecture**, where each service is responsible for a specific function:

1. **API Gateway**: Acts as the entry point for clients, forwarding requests to the **Location Service** and **Weather Service**. It aggregates data from both services and returns a unified response.
2. **Weather Service**: Fetches weather information based on geographic coordinates (latitude and longitude). This service queries a third-party weather API to retrieve real-time weather data.
3. **Location Service**: Resolves city names into geographic coordinates (latitude and longitude). This service can be extended to support more accurate or real-time city lookup methods.

### Service Flow

1. **Client Request**: The client sends a request to the **API Gateway** asking for the weather of a city.
2. **Location Resolution**: The **API Gateway** calls the **Location Service** to resolve the city name into latitude and longitude.
3. **Weather Data Fetch**: The **API Gateway** then calls the **Weather Service** to fetch weather data using the coordinates obtained from the **Location Service**.
4. **Response**: The **API Gateway** combines the weather data and sends it back to the client.

---

## Services

### 1. **API Gateway**

The **API Gateway** is responsible for receiving client requests, calling the necessary services, and returning the response. It acts as the central controller for the system.

#### Endpoints:
- **`GET /weather?city=<city_name>`**
  - **Description**: Receives a city name and returns the real-time weather data by calling the **Location Service** and **Weather Service**.
  - **Parameters**:
    - `city`: The name of the city for which weather information is requested.
  - **Response Example**:
    ```json
    {
      "temp": 15.0,
      "humidity": 80,
      "description": "clear sky"
    }
    ```

### 2. **Weather Service**

The **Weather Service** is responsible for fetching weather data from a third-party weather API using the latitude and longitude of a location.

#### Endpoints:
- **`GET /weather?lat=<latitude>&lon=<longitude>`**
  - **Description**: Accepts latitude and longitude and returns the weather information for the specified coordinates.
  - **Parameters**:
    - `lat`: Latitude of the location.
    - `lon`: Longitude of the location.
  - **Response Example**:
    ```json
    {
      "temp": 15.0,
      "humidity": 80,
      "description": "clear sky"
    }
    ```

### 3. **Location Service**

The **Location Service** resolves a city name to its corresponding latitude and longitude. In this version, it uses a simple internal mapping, but it can be expanded to use external geolocation APIs for better accuracy.

#### Endpoints:
- **`GET /location?city=<city_name>`**
  - **Description**: Resolves a city name into geographic coordinates (latitude and longitude).
  - **Parameters**:
    - `city`: The name of the city.
  - **Response Example**:
    ```json
    {
      "lat": 40.7128,
      "lon": -74.0060
    }
    ```

---

## Setup and Installation

### Prerequisites

Before you begin, ensure you have the following installed:
- **Docker** and **Docker Compose**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.9+** (for local development without Docker)
- **pip** (Python's package installer)

### Running the Application with Docker

To run the entire application using **Docker Compose**, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/real-time-weather-api.git
   cd real-time-weather-api
   ```

2. **Build and start the containers**:

   Run the following command in the root directory of the project to build and run the services:

   ```bash
   docker-compose up --build
   ```

3. **Access the services**:
   - **API Gateway**: `http://localhost:5000`
   - **Weather Service**: `http://localhost:5001`
   - **Location Service**: `http://localhost:5002`

4. **Stopping the Application**:
   To stop the services and remove the containers, run:

   ```bash
   docker-compose down
   ```

---

## Running the Weather Service Individually

If you wish to run only the **Weather Service** without the other services, you can do so by following these steps:

1. **Navigate to the `weather_service` directory**:

   ```bash
   cd weather_service
   ```

2. **Build the Docker image**:

   ```bash
   docker build -t weather_service .
   ```

3. **Run the container**:

   ```bash
   docker run -d -p 5001:5001 --name weather_service weather_service
   ```

4. **Test the Weather Service**:

   You can test the weather service by sending requests to `http://localhost:5001` with coordinates.

---

## Testing

To test the individual services, the project includes **pytest** tests for each service.

1. **Install pytest**:
   
   ```bash
   pip install pytest pytest-mock
   ```

2. **Run all tests**:

   Run the following command in the project root directory to execute tests for all services:

   ```bash
   pytest
   ```

3. **Run tests for a specific service**:

   ```bash
   pytest weather_service/tests/
   pytest location_service/tests/
   pytest gateway/tests/
   ```

---

## Contributing

We welcome contributions to improve the Real-Time Weather API. To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push your changes (`git push origin feature-name`).
5. Create a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- The **Weather Service** fetches weather data from a third-party API like **OpenWeatherMap** (this can be easily integrated by modifying the service to call the API).
- The **Location Service** is a simple resolver for city names to coordinates. It can be extended with external services like **Google Maps Geocoding API** for more accurate results.

---

This README file provides a comprehensive explanation of the **Real-Time Weather API** framework, covering the architecture, service details, installation, and usage instructions.
# KPI Project

This project is a Django REST API application for managing KPIs (Key Performance Indicators) and Assets. It allows you to create KPIs, assign them to Assets, and evaluate KPI expressions with input values. The application is structured using Django REST Framework and adheres to the SOLID principles.

## Project Structure

kpi_project/ │ ├── kpi_project/ # Main project directory │ ├── init.py │ ├── asgi.py │ ├── settings.py # Django settings │ ├── urls.py # Project URLs │ └── wsgi.py │ ├── kpi_app/ # Application directory │ ├── init.py │ ├── admin.py # Register models for admin interface │ ├── apps.py │ ├── models.py # Contains models for KPI, Asset, and AssetKPI │ ├── serializers.py # Serializers for API output │ ├── urls.py # Application-specific URLs │ ├── views.py # API views for KPI, Asset, and AssetKPI │ ├── utils.py # Utility functions, including EquationEvaluator │ └── tests.py # Unit tests for the API │ ├── db.sqlite3 # SQLite database file └── manage.py # Django management script


## Setting Up the Project Locally

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)
- Django and Django REST Framework

### Installation Steps

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd kpi_project
    ```

2. **Set up a virtual environment** (optional):
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install django djangorestframework
    ```

4. **Run migrations** to set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

The server should now be running at `http://localhost:8000`.

## API Usage (Testing with Postman)

Follow these steps to test the API using Postman:

### 1. Create a KPI

- **Endpoint**: `POST http://localhost:8000/api/kpis/`
- **Body (JSON)**:
    ```json
    {
        "name": "Temperature KPI",
        "expression": "ATTR + 10",
        "description": "Example KPI for temperature"
    }
    ```
- **Expected Response**:
    ```json
    {
        "id": 1,
        "name": "Temperature KPI",
        "expression": "ATTR + 10",
        "description": "Example KPI for temperature"
    }
    ```

### 2. Create an Asset

- **Endpoint**: `POST http://localhost:8000/api/assets/`
- **Body (JSON)**:
    ```json
    {
        "asset_id": "Asset123",
        "name": "Temperature Sensor"
    }
    ```
- **Expected Response**:
    ```json
    {
        "id": 1,
        "asset_id": "Asset123",
        "name": "Temperature Sensor"
    }
    ```

### 3. Link the KPI to the Asset

- **Endpoint**: `POST http://localhost:8000/api/asset-kpis/`
- **Body (JSON)**:
    ```json
    {
        "kpi": 1,
        "asset": 1,
        "attribute_id": "Temp"
    }
    ```
- **Expected Response**:
    ```json
    {
        "id": 1,
        "kpi": 1,
        "asset": 1,
        "attribute_id": "Temp"
    }
    ```

### 4. Evaluate the KPI with a Specific Value

- **Endpoint**: `POST http://localhost:8000/api/asset-kpis/1/evaluate/`
- **Body (JSON)**:
    ```json
    {
        "value": 20
    }
    ```
- **Expected Response** (based on expression `ATTR + 10`):
    ```json
    {
        "result": 30
    }
    ```

## Testing with `message.txt` File

Suppose `message.txt` contains multiple JSON records (messages) representing sensor readings that need to be evaluated. Each message should be formatted as follows:

```json
{"asset_id": "Asset123", "attribute_id": "Temp", "timestamp": "2022-07-31T23:28:37Z[UTC]", "value": 20}
Example of Processing Each Line
To process the file, you could write a Python script that reads each line, extracts the value, and calls the /evaluate/ endpoint with that value. Here’s a sample script:
import requests
import json

# Path to the message.txt file
file_path = 'message.txt'

# Endpoint for evaluating KPI expressions
url = 'http://localhost:8000/api/asset-kpis/1/evaluate/'

with open(file_path, 'r') as file:
    for line in file:
        message = json.loads(line)
        value = message.get('value')

        # Send the value to the API
        response = requests.post(url, json={"value": value})
        print(f"Input: {value}, Output: {response.json()}")
Expected Output for Each Case
Given the expression ATTR + 10:

Input: {"value": 20} → Expected Output: {"result": 30}
Input: {"value": 15} → Expected Output: {"result": 25}
Input: {"value": 5} → Expected Output: {"result": 15}
This script will read each message in message.txt, send the value to the API, and print the evaluated result.

Additional Notes
Make sure the Django server is running before testing with Postman or the message.txt script.
You can extend the project by adding more KPI expressions or assets as needed.
For security, avoid using eval in production code; consider using a math parsing library if necessary.
This README provides an overview of the project structure, setup instructions, API usage, and an example script to test messages from a file. Let me know if you need further customization!

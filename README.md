(
# KPI Project

This project is a Django REST API application for managing KPIs (Key Performance Indicators) and Assets. It allows you to create KPIs, assign them to Assets, and evaluate KPI expressions with input values. The application is structured using Django REST Framework and adheres to the SOLID principles.

## Project Structure

```
kpi_project/
│
├── kpi_project/                # Main project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Project URLs
│   └── wsgi.py
│
├── kpi_app/                    # Application directory
│   ├── __init__.py
│   ├── admin.py                # Register models for admin interface
│   ├── apps.py
│   ├── models.py               # Contains models for KPI, Asset, and AssetKPI
│   ├── serializers.py          # Serializers for API output
│   ├── urls.py                 # Application-specific URLs
│   ├── views.py                # API views for KPI, Asset, and AssetKPI
│   ├── utils.py                # Utility functions, including EquationEvaluator
│   └── tests.py                # Unit tests for the API
│
├── db.sqlite3                  # SQLite database file
└── manage.py                   # Django management script
```

## Setting Up the Project Locally

### Prerequisites

- Python 3.13
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
    source env/bin/activate  # On Windows use `env\Scriptsctivate`
    ```

3. **Install dependencies**:
    ```bash
    pip install django djangorestframework drf-yasg
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

## Using Swagger for API Testing

To make API testing easier, Swagger provides a UI for exploring and interacting with the APIs.

1. **Set up Swagger**:
    - Add Swagger to the project by configuring it in `kpi_project/urls.py` as follows:

    ```python
    # kpi_project/urls.py

    from django.contrib import admin
    from django.urls import path, include
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions

    schema_view = get_schema_view(
        openapi.Info(
            title="KPI API",
            default_version='v1',
            description="API for managing KPIs and Assets",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('kpi_app.urls')),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
    ```

2. **Access the Swagger UI**:
    - Go to `http://localhost:8000/swagger/` in your browser.
    - You’ll see a UI that allows you to interact with the available endpoints, including creating, linking, and evaluating KPIs.

## API Usage (Testing with Postman)

Follow these steps to test the API manually using Postman:

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
{"asset_id": "Asset123", "attribute_id": "Temp", "timestamp": "2024-10-31T10:00:00Z", "value": "20"}
{"asset_id": "Asset123", "attribute_id": "Temp", "timestamp": "2024-10-31T10:05:00Z", "value": "30"}
{"asset_id": "Asset123", "attribute_id": "Temp", "timestamp": "2024-10-31T10:00:00Z", "value": "20"}
```

### Command to Process the Whole file at once
```
python manage.py process_messages kpi_app/message.txt
```

## Additional Notes

- Make sure the Django server is running before testing with Postman, Swagger, or the `message.txt` script.
- You can extend the project by adding more KPI expressions or assets as needed.

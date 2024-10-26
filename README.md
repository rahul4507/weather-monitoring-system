# Real-Time Weather Monitoring System

## Project Overview
A Django-based real-time weather monitoring system that tracks weather conditions across major Indian metros using OpenWeatherMap API. The system uses Django Q for task scheduling and provides weather summaries, alerts, and data processing capabilities.

## Tech Stack
### Backend
- Django 4.2
- Django REST Framework
- Django Q (for task scheduling)
- PostgreSQL/SQLite3
- Django Environ (for environment variables)

### Key Components
- Django Q Cluster for scheduled tasks
- Server-Sent Events (SSE) for real-time updates
- OpenWeatherMap API integration
- CORS support for frontend integration

## Prerequisites
- Python 3.8+
- PostgreSQL (optional, SQLite3 included by default)
- Redis (for Django Q)
- OpenWeatherMap API key

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd weather-monitoring
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create .env file in project root
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3  # Or your PostgreSQL URL
API_KEY=your-openweathermap-api-key
CITIES=Delhi,Mumbai,Chennai,Bangalore,Kolkata,Hyderabad
INTERVAL=5  # Weather update interval in minutes
SSE_DELAY=1  # Server-Sent Events delay in seconds
```

5. Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Start Django Q cluster (in a separate terminal)
```bash
python manage.py qcluster
```

8. Schedule weather tasks
```bash
python manage.py schedule_weather_tasks
```

9. Run development server
```bash
python manage.py runserver
```

## Project Structure
```
weather_monitoring/
├── app/
│   ├── settings.py      # Project settings
│   ├── urls.py         # URL configurations
│   └── wsgi.py         # WSGI configuration
├── weather_dashboard/
│   ├── models/         # Database models
│   ├── views/          # API views
│   ├── tasks/          # Django Q tasks
│   └── utils/          # Helper functions
├── manage.py
├── requirements.txt
└── .env
```

## Configuration Details

### Django Settings
Key configurations in `settings.py`:
- Django Q cluster settings for task management
- CORS configuration for frontend integration
- OpenWeatherMap API settings
- Database configuration
- Environment variables handling

### Django Q Configuration
```python
Q_CLUSTER = {
    'name': 'DjangoQ',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'django_redis': 'default',
    'scheduler': 'django_q.schedule',
    'bulk': 10,
    'orm': 'default',
}
```

### Alert System
- Alerts are logged to the Django Q console
- Configurable thresholds for temperature monitoring
- Real-time alert generation for threshold breaches

## API Endpoints
- List of available endpoints and their functionality
- Authentication requirements (if any)
- Request/Response formats

## Dependencies
```
Django==4.2.16
django-environ==0.11.2
django-q==1.3.9
djangorestframework==3.15.2
psycopg2-binary==2.9.10
redis==3.5.3
requests==2.32.3
... (other dependencies as listed in requirements.txt)
```

## Running the System
1. Ensure all services are running:
   - Redis server (for Django Q)
   - PostgreSQL (if using)
   - Django development server
   - Django Q cluster

2. Start all required processes:
```bash
# Terminal 1: Run Django Q cluster
python manage.py qcluster

# Terminal 2: Run Django development server
python manage.py runserver

# One-time setup: Schedule weather tasks
python manage.py schedule_weather_tasks
```

## Monitoring and Debugging
- Django Q admin interface (`/admin/django_q/`)
- Console output for alerts and task execution
- Django debug toolbar in development

## Error Handling
- API error responses
- Task failure handling in Django Q
- Data validation and error logging


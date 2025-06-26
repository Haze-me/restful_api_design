
### RESTful API design with best practices;

A robust Task Management RESTful API built with Django and Django REST Framework featuring:
- JWT Authentication
- Comprehensive error handling
- API documentation with Swagger/Redoc
- Logging
- Unit and integration tests


### Prerequisites:
Before you begin, ensure you have the following installed:
- Python 3.8+
- pip
- virtualenv (recommended)

### Local Development Setup:

1. Clone repo
git clone https://github.com/Haze-me/restful_api_design.git

   cd restful_api_design

2. Set virtual enviroment (recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```
## Requirements:
- Python 3.8+
- Django 5.0+
- Other dependencies (list them here)

3. Install Dependencies
```bash
   pip install -r requirements.txt
```


## Run Migrations

4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

The API will be available at http://localhost:8000/api/

## API Documentation:
After starting the server, access the interactive documentation:

Swagger UI: http://localhost:8000/api/docs/

ReDoc: http://localhost:8000/api/redoc/

- Access Doc folder for API_DOCUMENTATION

## Testing
- Access Doc folder for TESTING on how to run test and code coverage
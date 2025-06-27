
### RESTful API design with best practices;

A robust Task Management RESTful API built with Django and Django REST Framework featuring:
- JWT Authentication
- Comprehensive error handling
- API documentation with Swagger/Redoc
- Logging
- Unit and integration tests


### Prerequisites:
Before you begin, ensure you have the following installed:

- Python 3.13.5   (make sure the python is the latest version) `python3 --version`

- pip 25.1.1   ```pip install --upgrade pip``` (recommended to upgrade pip)

- virtualenv (recommended)

NB:
   Windows:
   - Download the latest Python installer from `python.org`

   - Run the installer and check:

   - "Add Python to PATH" (important!)

   - `python3 --version`

   Linux (Debian/Ubuntu):

   - `sudo apt update`

   - `sudo apt install python3`

   - `python3 --version`

   On macOS
  
   - `brew update`

   - `brew install python`

   - `python3 --version`



### Local Development Setup:

1. Clone repo
`git clone https://github.com/Haze-me/restful_api_design.git`

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

- asgiref==3.8.1
- Django==5.2
- djangorestframework==3.14.0
- python-dotenv==1.0.0
- dj-database-url==3.0.0
- django-filter==25.1
- djangorestframework_simplejwt==5.5.0
- PyJWT==2.7.0
- drf-spectacular==0.26.3
- drf-spectacular-sidecar==2023.5.1
- django-cors-headers==4.4.0  # More Windows-friendly


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

5. Create a superuser (optional): to access Admin panal http://localhost:8000/admin/

   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```


## API Documentation:
After starting the server, access the interactive documentation:

Swagger UI: http://localhost:8000/api/docs/

ReDoc: http://localhost:8000/api/redoc/

- For guide on how to test the `API` using `POSTMAN` Access Doc folder for API_DOCUMENTATION

## Testing
- Access Doc folder for TESTING on how to run test and code coverage
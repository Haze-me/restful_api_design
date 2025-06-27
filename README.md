
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


# Code Test

To run tests with coverage:
```bash
coverage run manage.py test
coverage html
```
- Then it going generate a folder called 'htmlcov' in the root directory, in there you can run it as html in your browser


## API Documentation:
After starting the server, access the interactive documentation:

Swagger UI: http://localhost:8000/api/docs/

ReDoc: http://localhost:8000/api/redoc/

- For guide on how to test the `API` using `POSTMAN`


# Task Manager API - Postman Testing Guide:


### Environment Setup

## Create a new environment in Postman named "Task Manager API"

- Add these variables:
   ```plaintext
   base_url = http://localhost:8000/api
   access_token = {{leave empty}}
   refresh_token = {{leave empty}}
  ```
## Tests/Scripts Tab:
- add this javascript:

```
pm.test("Task created", () => {
    pm.response.to.have.status(201);
    const taskId = pm.response.json().data.id;
    pm.environment.set("task_id", taskId);
});
```


### 1.Authentication Workflow

1.1 Register New User
```
POST {{base_url}}/auth/register/
Content-Type: application/json
```

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123",
  "password2": "testpass1234"
}
```


1.2 Login & Get Tokens
```
POST {{base_url}}/auth/token/
Content-Type: application/json
```

```json
{
  "email": "test@example.com",
  "password": "testpass1234"
}
```

1.3 Refresh Access Token

```
POST {{base_url}}/auth/token/refresh/
Content-Type: application/json
```
```json
{
  "refresh": "{{refresh_token}}"
}
```

### 2.Task Management

2.1 Create New Task

```
POST {{base_url}}/tasks/
Authorization: Bearer {{access_token}}
Content-Type: application/json
```
```json
{
  "title": "Complete Postman testing",
  "description": "Write all test cases",
  "status": "todo",
  "due_date": "2025-12-31T23:59:00Z"
}
```

2.2 Get All Tasks
```
GET {{base_url}}/tasks/
Authorization: Bearer {{access_token}}
```

2.3 Update Task
```
PATCH {{base_url}}/tasks/{{task_id}}/
Authorization: Bearer {{access_token}}
Content-Type: application/json
```
```json
{
  "status": "in_progress"
}
```

2.4 Delete Task
```
DELETE {{base_url}}/tasks/{{task_id}}/
Authorization: Bearer {{access_token}}
```

## 3. Error Testing

3.1 Invalid Credentials
```
POST {{base_url}}/auth/token/
Content-Type: application/json
```

```json
{
  "email": "wrong@example.com",
  "password": "wrongpass"
}
```
Expected: 401 Unauthorized

3.2 Missing Authentication:

```
GET {{base_url}}/tasks/
```

Expected: 401 Unauthorized


4.3 Invalid Task Data
```
POST {{base_url}}/tasks/
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

```json
{
  "title": "",
  "status": "invalid_status"
}
```
Expected: 400 Bad Request


### Test Automation
# Collection Runner Setup
Create new collection "Task Manager Tests"

Add requests in this order:

- Register

- Login

- Get Tasks

- Update Task

- Delete Task

- Set delay between requests: 300ms

### Test/scrips Script Examples For Login Request:

- Add this javascript at the test or scripts tap;

```
pm.test("Status code is 200", () => pm.response.to.have.status(200));
pm.test("Response has tokens", () => {
    const jsonData = pm.response.json();
    pm.expect(jsonData.access).to.be.a('string');
    pm.expect(jsonData.refresh).to.be.a('string');
});
```


6. Common Issues & Solutions
Issue	Solution
- 401 Errors	Verify tokens are set in environment
- 500 Errors	Check server logs for exceptions
- Connection Refused	Ensure Django server is running
- Invalid Date Format	Use ISO8601: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ 

## Full Test Scenario

Positive Flow:

- Register → 201

- Login → 200 (store tokens)

- Create Task → 201 (store task_id)

- List Tasks → 200 (verify presence)

- Update Task → 200

- Delete Task → 200

- Verify Deletion → 200 (empty list)

Negative Flow:

- Invalid Registration → 400

- Wrong Login → 401

- Create Task Unauthenticated → 401

- Update Non-Existent Task → 404



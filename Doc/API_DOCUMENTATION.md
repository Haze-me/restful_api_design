
# Task Manager API - Postman Testing Guide:


### Environment Setup

## Create a new environment in Postman named "Task Manager API"

- Add these variables:
   ```plaintext
   base_url = http://localhost:8000/api
   access_token = {{leave empty}}
   refresh_token = {{leave empty}}

## Tests/Scripts Tab:
- add this javascript:

```json
pm.test("Task created", () => {
    pm.response.to.have.status(201);
    const taskId = pm.response.json().data.id;
    pm.environment.set("task_id", taskId);
});
```


### 1.Authentication Workflow

1.1 Register New User
http
POST {{base_url}}/auth/register/
Content-Type: application/json

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123",
  "password2": "testpass1234"
}
```


1.2 Login & Get Tokens
http
POST {{base_url}}/auth/token/
Content-Type: application/json

```json
{
  "email": "test@example.com",
  "password": "testpass1234"
}
```

1.3 Refresh Access Token

http
POST {{base_url}}/auth/token/refresh/
Content-Type: application/json

```json
{
  "refresh": "{{refresh_token}}"
}
```

### 2.Task Management

2.1 Create New Task

http
POST {{base_url}}/tasks/
Authorization: Bearer {{access_token}}
Content-Type: application/json

```json
{
  "title": "Complete Postman testing",
  "description": "Write all test cases",
  "status": "todo",
  "due_date": "2025-12-31T23:59:00Z"
}
```

2.2 Get All Tasks
http
GET {{base_url}}/tasks/
Authorization: Bearer {{access_token}}


2.3 Update Task
http
PATCH {{base_url}}/tasks/{{task_id}}/
Authorization: Bearer {{access_token}}
Content-Type: application/json

```json
{
  "status": "in_progress"
}
```

2.4 Delete Task
http
DELETE {{base_url}}/tasks/{{task_id}}/
Authorization: Bearer {{access_token}}


## 3. Error Testing

3.1 Invalid Credentials
http
POST {{base_url}}/auth/token/
Content-Type: application/json

```json
{
  "email": "wrong@example.com",
  "password": "wrongpass"
}
```
Expected: 401 Unauthorized

3.2 Missing Authentication
http
GET {{base_url}}/tasks/

Expected: 401 Unauthorized


4.3 Invalid Task Data
http
POST {{base_url}}/tasks/
Authorization: Bearer {{access_token}}
Content-Type: application/json

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

```json
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


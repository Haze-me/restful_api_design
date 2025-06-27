
# API Endpoints


## Authentication
### `POST /api/auth/register/`
- To Register a new user.

Request Body:

{
  "username": "string",
  "email": "string",
  "password": "string",
  "password2": "string"
}

Response

{
    "success": true,
    "status_code": 201,
    "message": "Success",
    "data": {
        "id": 3,
        "username": "test123",
        "email": "test@gmail.com",
        "bio": null,
        "date_joined": "2025-06-26T02:36:09.284826Z"
    }
}

## `POST /api/auth/token/` 
- To Login and obtain JWT tokens.

Request Body:
{
  "email": "test@gmail.com",
  "password": "test123"
}

Response:
{
  "access": "string",
  "refresh": "string",
  "user": { /* user data */ } 
  // NB: it will generate an access_token, for user authentication
}

## Creating Task

## `POST /api/tasks/`
- To Create a new task.

Request Body:
{
  "title": "string",
  "description": "string",
  "status": "string",
  "due_date": "ISO8601"
}

Response:
{
    "success": true,
    "status_code": 201,
    "message": "Success",
    "data": {
        "id": 3,
        "title": "Testing some codes project",
        "description": "Done doing it",
        "status": "todo",
        "due_date": "2027-11-11T00:00:00Z",
        "user": 3,
        "created_at": "2025-06-26T02:40:38.924287Z",
        "updated_at": "2025-06-26T02:40:38.924324Z"
    }
}


## `GET /api/tasks/`
- List all tasks for a user (authenticated user only).

Query Params:
- status: Filter by status (todo/in_progress/done)
- due_date_from: Filter by start date
- due_date_to: Filter by end date



## `PUT /api/tasks/{id}/`
- To Update task.

Request Body:
{
    "title": "Updated Task Title",
    "description": "codes working fine now",
    "status": "done",
    "due_date": "2025-09-15"
}

Response:
{
    "success": true,
    "status_code": 200,
    "message": "Success",
    "data": {
        "id": 3,
        "title": "Updated Task Title",
        "description": "codes working fine now",
        "status": "done",
        "due_date": "2025-09-15T00:00:00Z",
        "user": 3,
        "created_at": "2025-06-26T02:40:38.924287Z",
        "updated_at": "2025-06-26T11:31:43.157194Z"
    }
}

## `DELETE /api/tasks/{id}/`
- To Delete task:


Response:
{
    "success": true,
    "status_code": 200,
    "message": "Task deleted successfully",
    "data": null
}
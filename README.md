# Task Management API

A RESTful Task Management API built with Django and Django REST Framework. It provides user registration, JWT-based authentication, and task CRUD operations with per-user access control.

## Features

- User registration with password validation and password hashing.
- JWT authentication with access and refresh tokens.
- Create, list, retrieve, update, and delete tasks.
- Task ownership enforcement: users can access only their own tasks.
- Task status choices: `pending`, `in_progress`, and `completed`.
- Optional task descriptions and due dates.
- Automated API tests for core functionality and access control.
- Postman collection for manual API testing.
- SQLite for local development.

## Technology Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite
- Postman

## Project Structure

```text
task-management-api/
├── README.md
├── .gitignore
├── postman/
│   └── Task-Management-API.postman_collection.json
└── backend/
    ├── manage.py
    ├── requirements.txt
    ├── .env.example
    ├── config/
    ├── accounts/
    ├── tasks/
    └── db.sqlite3  # Created locally; not committed
```

## Requirements

- Python 3.10 or newer, compatible with the project's installed dependencies.
- Git
- Postman (optional, for manual API testing)

## Local Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd task-management-api
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create and activate a virtual environment

From the repository root:

```bash
python -m venv backend/env
```

Windows Command Prompt:

```bat
backend\env\Scripts\activate
```

If activation does not work from your current directory, activate it using the appropriate path for your shell.

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure environment variables

Review `backend/.env.example` and configure the required environment variables if the project settings use them.

Do not commit real secrets or production credentials.

### 5. Apply database migrations

```bash
cd backend
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

All endpoints below assume the local development server is running.

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | Public | Register a user |
| POST | `/api/auth/login/` | Public | Obtain access and refresh tokens |
| POST | `/api/auth/token/refresh/` | Public | Obtain a new access token |
| GET | `/api/tasks/` | Required | List the authenticated user's tasks |
| POST | `/api/tasks/` | Required | Create a task |
| GET | `/api/tasks/{id}/` | Required | Retrieve an owned task |
| PUT | `/api/tasks/{id}/` | Required | Replace an owned task's editable fields |
| PATCH | `/api/tasks/{id}/` | Required | Partially update an owned task |
| DELETE | `/api/tasks/{id}/` | Required | Delete an owned task |

Authenticated requests must include:

```http
Authorization: Bearer <access_token>
```

## Authentication Examples

### Register

`POST /api/auth/register/`

```json
{
  "username": "demo_user",
  "email": "demo@example.com",
  "password": "StrongDemoPass123!"
}
```

Use a unique email address for each registration. The example password is for demonstration only.

### Log in

`POST /api/auth/login/`

```json
{
  "username": "demo_user",
  "password": "StrongDemoPass123!"
}
```

The response contains an access token and a refresh token. Use the access token for protected endpoints.

### Refresh an access token

`POST /api/auth/token/refresh/`

```json
{
  "refresh": "<refresh_token>"
}
```

## Task Examples

### Create a task

`POST /api/tasks/`

```json
{
  "title": "Complete project documentation",
  "description": "Prepare the API README and test the endpoints",
  "status": "pending",
  "due_date": "2026-11-01"
}
```

The `title` is required. The description and due date are optional. The status defaults to `pending`.

### Update a task

`PATCH /api/tasks/1/`

```json
{
  "status": "completed"
}
```

Replace `1` with the ID of a task you own.

## Security and Access Control

- Passwords are hashed using Django's user creation API.
- Protected endpoints require JWT authentication.
- Task ownership is assigned from the authenticated user, not from client-supplied user IDs.
- Task queries are filtered by the authenticated user.
- Requests to retrieve, update, or delete another user's task return `404 Not Found`.
- Password validation follows Django's configured password validators.

## Running Tests

From the `backend/` directory:

```bash
python manage.py check
python manage.py test tasks
```

The tests verify task creation, listing, updating, deletion, authentication requirements, and cross-user access restrictions.

## Postman Collection

Import `postman/Task management api.postman_collection.json` into Postman to test the API endpoints.

Start the local server before running the requests. Register or use a local demo account, log in to obtain a token, and send the access token with protected requests.

## Current Scope

This project provides a Django REST API with SQLite-based local development. It does not include a frontend application.

For production deployment, configure secure environment variables, an appropriate production database, HTTPS, and production-grade Django settings.

## License

Add a license if you intend to distribute this project under a specific open-source license.
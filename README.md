# simple-task-manager-185050-185059

Django REST API for a Todo app with JWT authentication using Django REST Framework and SimpleJWT.

## Setup

- Python 3.12+
- Install dependencies:
  pip install -r requirements.txt

- Run migrations:
  cd todo_backend
  python manage.py migrate
  python manage.py createsuperuser  # optional

- Start server:
  python manage.py runserver 0.0.0.0:8000

## Auth Endpoints

- POST /auth/register
  Body: {"username":"alice","email":"a@example.com","password":"Passw0rd!","password_confirm":"Passw0rd!"}

- POST /auth/login
  Body: {"username":"alice","password":"Passw0rd!"}
  Response: {"access":"...","refresh":"..."}

- POST /auth/refresh
  Body: {"refresh":"<refresh_token>"}

- POST /auth/logout
  Body: {"refresh":"<refresh_token>"}  # best effort blacklist

- GET /auth/me
  Header: Authorization: Bearer <access>

## Todos (protected)

Base path: /api/todos/

- Create:
  curl -X POST http://localhost:8000/api/todos/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS" \
    -d '{"title":"Buy milk","description":"2%"}'

- List (only your todos):
  curl -H "Authorization: Bearer $ACCESS" http://localhost:8000/api/todos/

- Update:
  curl -X PATCH http://localhost:8000/api/todos/1/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS" \
    -d '{"completed": true}'

- Delete:
  curl -X DELETE http://localhost:8000/api/todos/1/ \
    -H "Authorization: Bearer $ACCESS"

## Environment variables

Create a .env or set environment variables (optional):

- DJANGO_SECRET_KEY: Secret key for Django (default is development value)
- DJANGO_DEBUG: "true" or "false" (default: true)
- JWT_SECRET_KEY: Secret for JWT signing (defaults to SECRET_KEY)

Example .env.example:
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=true
JWT_SECRET_KEY=change-me-too

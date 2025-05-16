# Blog API Project

A REST API built with FastAPI that enables user management and blog post functionality with JWT authentication.

## Technologies Used

- FastAPI
- SQLAlchemy (ORM)
- Pydantic
- JWT Authentication
- Uvicorn (ASGI server)

## System Requirements

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate virtual environment:
```bash
python -m venv blog-env
source blog-env/bin/activate  # For Linux/Mac
# or
.\blog-env\Scripts\activate  # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Project

1. Start the server:
```bash
uvicorn blog.main:app --reload
```

2. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
blog/
├── __init__.py
├── main.py              # Application entry point
├── database/           # Database configuration
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── routes/            # API endpoints
└── services/          # Business logic
```

## API Endpoints

- Authentication:
  - POST /auth/token: Login and get JWT token
  - POST /auth/register: Register new account

- Users:
  - GET /users/me: Get current user information
  - PUT /users/me: Update user information

- Blog:
  - GET /blogs: Get list of blog posts
  - POST /blogs: Create new blog post
  - GET /blogs/{id}: Get blog post details
  - PUT /blogs/{id}: Update blog post
  - DELETE /blogs/{id}: Delete blog post

## Security

- API uses JWT (JSON Web Tokens) for authentication
- Passwords are hashed using bcrypt
- CORS is configured to allow requests from frontend

## Development

To add new features:
1. Create model in `models/` directory
2. Create schema in `schemas/` directory
3. Add business logic in `services/` directory
4. Create routes in `routes/` directory
5. Register router in `main.py` 
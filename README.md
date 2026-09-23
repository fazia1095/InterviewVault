# InterviewVault

InterviewVault is a FastAPI-based interview preparation backend that provides user authentication, interview question management, quiz functionality, result tracking, and personalized dashboard statistics.

## Features

- User registration
- JWT-based authentication
- Secure password hashing with bcrypt
- Protected API endpoints
- Interview question CRUD operations
- Randomized quiz generation
- Quiz submission and automatic score calculation
- Quiz result history
- User-specific result access
- Personalized dashboard statistics
- SQLite database with SQLAlchemy ORM
- Automatic API documentation with Swagger UI

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- bcrypt
- Uvicorn

## Project Structure

```text
InterviewVault/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── dependencies.py
│   ├── auth_utils.py
│   │
│   └── routers/
│       ├── questions.py
│       ├── auth.py
│       ├── results.py
│       ├── quiz.py
│       └── dashboard.py
│
├── .gitignore
├── requirements.txt
└── README.md
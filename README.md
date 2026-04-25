# 🎓 Student Registry API :-

A RESTful API built with **FastAPI** and **PostgreSQL** for managing student records with secure JWT-based authentication. The system supports two user roles: *Stoners* (registered users/admins) and *Locals* (students being managed).

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Server](#running-the-server)
- [API Reference](#api-reference)
  - [Authentication](#authentication)
  - [Stoners (Users)](#stoners-users)
  - [Locals (Students)](#locals-students)
- [Authentication Flow](#authentication-flow)
- [Database Schema](#database-schema)
- [Security](#security)

---

## Overview

This API provides a complete CRUD interface for managing local student data. Access to student records is protected — only authenticated users (Stoners) can read, create, update, or delete student entries. User registration is open, and login issues a short-lived JWT access token.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.135.3 |
| Language | Python 3.12 |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0.49 |
| Validation | Pydantic v2 + pydantic-settings |
| Authentication | JWT (PyJWT 2.12.1) |
| Password Hashing | pwdlib 0.3.0 (Argon2) |
| ASGI Server | Uvicorn 0.44.0 |

---

## Project Structure

```
app/
├── __init__.py
├── main.py          # Application entry point, router registration
├── config.py        # Pydantic settings loaded from .env
├── database.py      # SQLAlchemy engine, session, and Base
├── models.py        # ORM table definitions (Student, Stoners)
├── schemas.py       # Pydantic request/response schemas
├── oauth2.py        # JWT creation and verification logic
├── utils.py         # Password hashing and verification
└── routers/
    ├── __init__.py
    ├── auth.py      # POST /login
    ├── locals.py    # CRUD for /locals (students)
    └── stoners.py   # POST /stoners (user registration)
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL (running locally or remotely)
- `pip` package manager

### Installation

**1. Clone the repository:**

```bash
git clone <your-repo-url>
cd <project-directory>
```

**2. Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root. **Do not commit this file to version control.**

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=FastAPI
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_secure_password

SECRET_KEY=your_random_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Tip:** Generate a strong `SECRET_KEY` with:
> ```bash
> openssl rand -hex 32
> ```

### Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive documentation is auto-generated at:
- **Swagger UI** → `http://127.0.0.1:8000/docs`
- **ReDoc** → `http://127.0.0.1:8000/redoc`

---

## API Reference

### Authentication

#### `POST /login`

Authenticates a registered user and returns a JWT access token.

**Request body** (`application/x-www-form-urlencoded`):

| Field | Type | Description |
|---|---|---|
| `username` | string | The user's email address |
| `password` | string | The user's password |

**Success response** `200 OK`:

```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

**Error responses:**
- `401 Unauthorized` — Invalid email or password

---

### Stoners (Users)

#### `POST /stoners/`

Registers a new user account. No authentication required.

**Request body** (`application/json`):

```json
{
  "name": "Jane Doe",
  "id": 1001,
  "sem": 4,
  "email": "jane@example.com",
  "password": "strongpassword"
}
```

**Success response** `201 Created`:

```json
{
  "name": "Jane Doe"
}
```

> Passwords are hashed with Argon2 before being stored. Plain-text passwords are never persisted.

---

### Locals (Students)

All `/locals` endpoints require a valid Bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

---

#### `GET /locals/`

Retrieves all student records.

**Success response** `200 OK`:

```json
[
  {
    "name": "Alice",
    "id": 1,
    "dept": "CSE",
    "sem": 3,
    "email": "alice@example.com"
  }
]
```

---

#### `GET /locals/{id}`

Retrieves a single student by ID.

**Path parameter:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | The student's unique ID |

**Success response** `200 OK` — returns a single `Student_Response` object.

**Error responses:**
- `404 Not Found` — Student with the given ID does not exist

---

#### `POST /locals/`

Creates a new student record.

**Request body** (`application/json`):

```json
{
  "name": "Bob Smith",
  "id": 42,
  "dept": "EEE",
  "sem": 2,
  "email": "bob@example.com"
}
```

**Success response** `200 OK` — returns the created `Student_Response` object.

---

#### `PUT /locals/{id}`

Updates an existing student record by ID.

**Path parameter:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | The student's unique ID |

**Request body** — same structure as `POST /locals/`.

**Success response** `200 OK` — returns the updated student object.

**Error responses:**
- `404 Not Found` — Student with the given ID does not exist

---

#### `DELETE /locals/{id}`

Deletes a student record by ID.

**Path parameter:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | The student's unique ID |

**Success response** `204 No Content` — record deleted successfully.

**Error responses:**
- `404 Not Found` — Student with the given ID does not exist

---

## Authentication Flow

```
1. Register        POST /stoners/      → create account
2. Login           POST /login         → receive access_token
3. Access resource GET /locals/        → pass Bearer token in Authorization header
4. Token expires   (after 30 minutes) → log in again to get a new token
```

The JWT payload contains the authenticated user's `user_id`. On each protected request, the token is verified and the corresponding `Stoners` record is fetched from the database to confirm the user still exists.

---

## Database Schema

### `local_student`

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | Primary Key, Indexed |
| `name` | VARCHAR | NOT NULL |
| `dept` | VARCHAR | NOT NULL |
| `sem` | INTEGER | NOT NULL |
| `email` | VARCHAR | NOT NULL |

### `stoners`

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | Primary Key, Indexed |
| `name` | VARCHAR | NOT NULL |
| `sem` | INTEGER | NOT NULL |
| `email` | VARCHAR | NOT NULL |
| `password` | VARCHAR | NOT NULL (hashed) |
| `created_at` | TIMESTAMP WITH TZ | NOT NULL, Default: `now()` |

Tables are created automatically via SQLAlchemy's `Base.metadata.create_all()` on startup.

---

## Security

- **Passwords** are hashed using Argon2 (via `pwdlib`) — a memory-hard algorithm resistant to brute-force attacks. Plain-text passwords are never stored.
- **JWT tokens** are signed with HS256 and expire after a configurable window (default: 30 minutes).
- **Credentials and secrets** are loaded exclusively from environment variables via `pydantic-settings` — never hardcoded in source files.
- **Protected routes** validate the Bearer token on every request and additionally verify that the token's user still exists in the database.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

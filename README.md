# Flask Backend with MVS Architecture

A complete Flask backend application using SQLAlchemy ORM with PostgreSQL database, following the Model-View-Service (MVS) architecture pattern.

## Features

- **MVS Architecture**: Clean separation of concerns with Models, Views, and Services
- **JWT Authentication**: Secure authentication with access and refresh tokens
- **PostgreSQL Database**: Robust database with SQLAlchemy ORM
- **User Management**: Complete CRUD operations for user management
- **Database Migrations**: Flask-Migrate for database schema management
- **CORS Support**: Cross-Origin Resource Sharing enabled
- **Environment Configuration**: Environment-based configuration management

## Project Structure

```
new-backend/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py              # User model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py      # Authentication business logic
│   │   └── user_service.py      # User business logic
│   └── views/
│       ├── __init__.py
│       ├── auth_views.py        # Authentication routes
│       └── user_views.py        # User routes
├── config.py                    # Configuration settings
├── app.py                       # Main application file
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── README.md                    # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### 2. Database Setup

1. Install PostgreSQL and create a database:
```sql
CREATE DATABASE your_database_name;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
```

2. Update the `.env` file with your database credentials:
```
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/your_database_name
```

### 3. Application Setup

1. Clone the repository and navigate to the project directory:
```bash
cd new-backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication

#### Register User
- **POST** `/api/auth/register`
- **Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Login
- **POST** `/api/auth/login`
- **Body:**
```json
{
  "username_or_email": "john_doe",
  "password": "secure_password"
}
```

#### Refresh Token
- **POST** `/api/auth/refresh`
- **Headers:** `Authorization: Bearer <refresh_token>`

#### Get Profile
- **GET** `/api/auth/profile`
- **Headers:** `Authorization: Bearer <access_token>`

### User Management

#### Get All Users
- **GET** `/api/users/?page=1&per_page=10`
- **Headers:** `Authorization: Bearer <access_token>`

#### Get User by ID
- **GET** `/api/users/<user_id>`
- **Headers:** `Authorization: Bearer <access_token>`

#### Create User
- **POST** `/api/users/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
  "username": "jane_doe",
  "email": "jane@example.com",
  "password": "secure_password",
  "first_name": "Jane",
  "last_name": "Doe"
}
```

#### Update User
- **PUT** `/api/users/<user_id>`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

#### Delete User
- **DELETE** `/api/users/<user_id>`
- **Headers:** `Authorization: Bearer <access_token>`

#### Deactivate User
- **PATCH** `/api/users/<user_id>/deactivate`
- **Headers:** `Authorization: Bearer <access_token>`

## Database Migration Commands

```bash
# Initialize migrations
flask db init

# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Downgrade migrations
flask db downgrade
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `JWT_SECRET_KEY` | JWT signing key | `jwt-secret-key` |
| `FLASK_ENV` | Environment mode | `development` |
| `FLASK_APP` | Main app file | `app.py` |

## Development

### Running Tests
```bash
# Add your test commands here
python -m pytest
```

### Code Style
Follow PEP 8 guidelines for Python code formatting.

## Architecture

### MVS Pattern

1. **Models** (`app/models/`): Database models using SQLAlchemy
2. **Views** (`app/views/`): HTTP request handlers and route definitions
3. **Services** (`app/services/`): Business logic and data processing

### Benefits of MVS Architecture:
- **Separation of Concerns**: Each layer has a specific responsibility
- **Testability**: Easy to unit test business logic in services
- **Maintainability**: Changes in one layer don't affect others
- **Scalability**: Easy to add new features following the same pattern

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License. 
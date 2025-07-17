# 🚀 Quick Start Guide - Flask Backend

This is a condensed version to get you up and running quickly!

## Prerequisites
- Python 3.8+
- PostgreSQL
- pip

## 1. Setup Environment

```bash
# Clone/navigate to project
cd new-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Database Setup

```bash
# Install PostgreSQL (macOS)
brew install postgresql@14
brew services start postgresql@14

# Create database
createdb flask_backend_db
```

## 3. Initialize Database

```bash
# Set Flask app
export FLASK_APP=app.py

# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

## 4. Run Application

```bash
# Start the server
python app.py
```

Your Flask backend is now running at: **http://localhost:5001**

## 5. Test API Endpoints

### Register a User
```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Login and Get Token
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "testuser",
    "password": "testpass123"
  }'
```

### Use Token for Protected Routes
```bash
# Replace TOKEN with actual token from login response
curl -X GET http://localhost:5001/api/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Available Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login user | No |
| GET | `/api/auth/profile` | Get user profile | Yes |
| GET | `/api/users/` | Get all users | Yes |
| GET | `/api/users/{id}` | Get user by ID | Yes |

## Environment Variables (.env)

```env
DATABASE_URL=postgresql+psycopg://bhaskarjoshi@localhost:5432/flask_backend_db
FLASK_ENV=development
FLASK_APP=app.py
```

**You're all set! 🎉**

For detailed documentation, see `DOCUMENTATION.md`. 
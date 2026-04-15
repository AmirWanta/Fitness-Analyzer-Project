# Fitness Analyzer API

A FastAPI backend for tracking and analyzing gym performance tailored towards powerlifting. 
Users can log workouts, record sets, and analyze performance over time. 

---

## Features

- User authentication with JWT tokens
- Create and manage workout sessions
- Log sets with reps, weight, and RPE
- Calculate estimated 1RM using the Epley formula
- Track progression of lifts over time
- RESTful API built with FastAPI
- Database managed with SQLAlchemy and Alembic
- Automated testing with Pytest

---

## Tech Stack

- FastAPI
- Python
- SQLAlchemy
- SQLite
- Alembic (migrations)
- Pytest (testing)

---

## Project Structure

- main.py – FastAPI app entry point
- endpoints.py – API routes
- tables.py – SQLAlchemy models
- schemas.py – Pydantic schemas
- database.py – DB connection setup
- security.py – authentication logic
- alembic/ – database migrations
- test.py – pytest tests

---

## How to Run Locally

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-folder>

2. Insatll dependencies

pip install -r requirements.txt

3. Run the server locaally

uvicorn main:app --reload

4. Open the swagger APi
http://127.0.0.1:8000/docs

---

## Usage

After starting the server, open the Swagger UI:

http://127.0.0.1:8000/docs

Follow this flow:

1. Create a user  
2. Login to get an access token  
3. Click "Authorize" and paste your token:
   Bearer <your_token>  
4. Create an exercise (e.g., Squat, Bench, Deadlift)  
5. Create a session  
6. Add sets to the session  
7. Use the analytics endpoints:
   - GET /users/{user_id}/exercises/{exercise_id}/1rm
   - GET /users/{user_id}/exercise/{exercise_id}/progress


  

from fastapi.testclient import TestClient
from main import app
import sqlite3

##testing database
"""conn = sqlite3.connect("powerlifting_project.db")
cursor = conn.execute("SELECT email, password FROM users")

for row in cursor:
    print(row)

"""

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={
        "email": "testuser1@example.com",
        "password": "password123",
        "unit": "lb",
        "training_mode": "powerlifting"
    })

    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "testuser1@example.com"
    assert data["unit"] == "lb"
    assert data["training_mode"] == "powerlifting"
    assert "id" in data    
 

def test_create_session():
    # 1. create user
    user_res = client.post("/users", json={
        "email": "sessionuser@example.com",
        "password": "password123",
        "unit": "lb",
        "training_mode": "powerlifting"
    })

    user_data = user_res.json()
    user_id = user_data["id"]

    # 2. login
    login_res = client.post("/login", json={
        "email": "sessionuser@example.com",
        "password": "password123"
    })

    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # 3. create session
    response = client.post("/sessions", json={
        "user_id": user_id,
        "date": "2026-04-14",
        "notes": "testing session"
    }, headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == user_id
    assert data["notes"] == "testing session"
    assert "id" in data


def test_add_set():
    user_res = client.post("/users", json={
        "email": "addsetuser@example.com",
        "password": "password123",
        "unit": "lb",
        "training_mode": "powerlifting"
    })

    user_data = user_res.json()
    user_id = user_data["id"]

    login_res = client.post("/login", json={
        "email": "addsetuser@example.com",
        "password": "password123"
    })

    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    session_res = client.post("/sessions", json={
        "user_id": user_id,
        "date": "2026-04-14",
        "notes": "testing session"
    }, headers=headers)

    sessData = session_res.json()
    sesIdData = sessData["id"]

    create_exer_res = client.post("/exercises", json={
        "name": "Squat"
    }, headers=headers)

    exercise_id = create_exer_res.json()["id"]

    addSetsRes = client.post(f"/sessions/{sesIdData}/sets", json={
        "exercise_id": exercise_id,
        "rpe": 6,
        "reps": 5,
        "weight": 200,
        "is_top_set": False
    }, headers=headers)

    data = addSetsRes.json()

    assert addSetsRes.status_code == 200
    assert data["session_id"] == sesIdData
    assert data["exercise_id"] == exercise_id
    assert data["reps"] == 5
    assert data["weight"] == 200


def test_1rm():
    user_res = client.post("/users", json={
        "email": "test1rmuser@example.com",
        "password": "pass123",
        "unit": "lb",
        "training_mode": "powerlifting"
    })

    user_data = user_res.json()
    user_id = user_data["id"]

    login_res = client.post("/login", json={
        "email": "test1rmuser@example.com",
        "password": "pass123"
    })

    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_exer_res = client.post("/exercises", json={
        "name": "Bench"
    }, headers=headers)

    exercise_id = create_exer_res.json()["id"]

    session_res = client.post("/sessions", json={
        "user_id": user_id,
        "date": "2026-04-14",
        "notes": "testing"
    }, headers=headers)

    sessData = session_res.json()
    session_id = sessData["id"]

    addSetsRes = client.post(f"/sessions/{session_id}/sets", json={
        "exercise_id": exercise_id,
        "rpe": 7,
        "reps": 8,
        "weight": 190,
        "is_top_set": False
    }, headers=headers)

    assert addSetsRes.status_code == 200

    response = client.get(
        f"/users/{user_id}/exercises/{exercise_id}/1rm",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()
    expected_1rm = 190 * (1 + 8 / 30)

    assert data["weight"] == 190
    assert data["reps"] == 8
    assert data["estimated_1rm"] == expected_1rm

def test_progress():
    user_res = client.post("/users", json={
        "email": "testprogressuser@example.com",
        "password": "pass123",
        "unit": "lb",
        "training_mode": "powerlifting"
    })

    user_data = user_res.json()
    user_id = user_data["id"]

    login_res = client.post("/login", json={
        "email": "testprogressuser@example.com",
        "password": "pass123"
    })

    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_exer_res = client.post("/exercises", json={
        "name": "Bench"
    }, headers=headers)

    exercise_id = create_exer_res.json()["id"]

    session_res = client.post("/sessions", json={
        "user_id": user_id,
        "date": "2026-04-14",
        "notes": "testing"
    }, headers=headers)

    session_id = session_res.json()["id"]

    session_res2 = client.post("/sessions", json={
        "user_id": user_id,
        "date": "2026-04-21",
        "notes": "testing 2"
    }, headers=headers)

    session_id2 = session_res2.json()["id"]

    addSetsRes = client.post(f"/sessions/{session_id}/sets", json={
        "exercise_id": exercise_id,
        "rpe": 7,
        "reps": 8,
        "weight": 190,
        "is_top_set": False
    }, headers=headers)

    assert addSetsRes.status_code == 200

    addSetsRes2 = client.post(f"/sessions/{session_id2}/sets", json={
        "exercise_id": exercise_id,
        "rpe": 8,
        "reps": 5,
        "weight": 200,
        "is_top_set": False
    }, headers=headers)

    assert addSetsRes2.status_code == 200

    response = client.get(
        f"/users/{user_id}/exercise/{exercise_id}/progress",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == user_id
    assert data["exercise_id"] == exercise_id
    assert "progress" in data
    assert len(data["progress"]) >= 2
    

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import models
import schemas
import crud

def test_create_user(client: TestClient, db_session: Session):
    user_data = {
        "email": "testuser1@example.com",
        "password": "testpassword"
    }
    response = client.post("/register/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]

    db_user = crud.get_user_by_email(db_session, email=user_data["email"])
    assert db_user is not None
    assert db_user.email == user_data["email"]

def test_login_user(client: TestClient, db_session: Session):
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/login/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data

def test_create_user_with_existing_email(client: TestClient, db_session: Session):
    user_data = {
        "email": "testuser@example.com",
        "password": "anotherpassword"
    }
    response = client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"message": "Email already registered"}

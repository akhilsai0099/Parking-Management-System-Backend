import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database import Base
from main import app, get_db

# Use an in-memory SQLite database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test database
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client

@pytest.fixture(scope="function")
def auth_token(client: TestClient, db_session: Session):
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    # Register the user
    client.post("/register/", json=user_data)
    # Login to get the token
    response = client.post("/login/", json=user_data)
    token = response.json()["token"]
    return token

# @pytest.fixture
# def parking_spot(client: TestClient, auth_token: str):
#     # Create a parking spot
#     spot_data = {
#         "level": 1,
#         "section": "A",
#         "spot_number": 3,
#         "vehicle_type": "car",
#         "exit_distance": 50,
#         "short_term_only": False,
#         "is_occupied": False,
#     }
#     headers = {"Authorization": auth_token}
#     response = client.post("/parking_spots/", json=spot_data, headers=headers)
#     assert response.status_code == 200
#     return response.json()

# @pytest.fixture
# def vehicle(client: TestClient, auth_token: str):
#     # Create a vehicle
#     vehicle_data = {
#         "license_plate": "ABC1238",
#         "vehicle_type": "car",
#         "owner_name": "John Doe",
#         "contact_number": "12345670"
#     }
#     headers = {"Authorization": auth_token}
#     response = client.post("/vehicles/", json=vehicle_data, headers=headers)
#     assert response.status_code == 201
#     return response.json()
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
def test_create_vehicle(client: TestClient, db_session: Session, auth_token: str):
    headers = {"Authorization": auth_token}
    print(headers)
    vehicle_data = {
        "license_plate": "ABC1234",
        "vehicle_type": "car",
        "owner_name": "John Doe",
        "contact_number": "1234567890"
    }

    response = client.post("/vehicles/", json=vehicle_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["license_plate"] == vehicle_data["license_plate"]

def test_get_vehicles(client: TestClient,  auth_token: str):
    headers = {"Authorization": auth_token}
    response = client.get("/vehicles/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_vehicle(client: TestClient, db_session: Session, auth_token: str):
    headers = {"Authorization": auth_token}
    vehicle_data = {
        "license_plate": "ABC1234",
        "vehicle_type": "car",
        "owner_name": "John Doe Updated",
        "contact_number": "1234567890"
    }

    response = client.put("/vehicles/6", json=vehicle_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Vehicle updated"

def test_delete_vehicle(client: TestClient, db_session: Session, auth_token: str):
    headers = {"Authorization": auth_token}
    response = client.delete("/vehicles/6", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Vehicle deleted"

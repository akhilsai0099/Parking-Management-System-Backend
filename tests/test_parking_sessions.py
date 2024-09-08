from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import models
import time



def test_create_parking_session(client, db_session, auth_token:str):
    
    header = {"Authorization": auth_token}
    vehicle = models.Vehicle(id=1, vehicle_type='Car', license_plate='ABC123', owner_id=1, owner_name='John Doe', contact_number='1234567890')
    db_session.add(vehicle)
    db_session.commit()

    
    spot = models.ParkingSpot(level=2, section='A', spot_number=1 ,vehicle_type='Car', is_occupied=False, short_term_only=False ,exit_distance=100)
    db_session.add(spot)
    db_session.commit()

    
    payload = {
        "vehicle_id": 1,
        "entry_time": (datetime.now()- timedelta(minutes=150)).isoformat(),
        "expected_exit_time": (datetime.now()+timedelta(minutes=15)).isoformat(),
    }

    response = client.post("/parking_sessions/", json=payload, headers=header)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Parking session created"


def test_get_parking_sessions(client: TestClient, auth_token: str):
    headers = {"Authorization": auth_token}
    response = client.get("/parking_sessions/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_calculate_price_and_exit(client: TestClient, auth_token: str):
    headers = {"Authorization": auth_token}
    response = client.put("/parking_sessions/1/price", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 11

def test_delete_parking_session(client: TestClient, auth_token: str):
    headers = {"Authorization": auth_token}
    response = client.delete("/parking_sessions/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parking session deleted"

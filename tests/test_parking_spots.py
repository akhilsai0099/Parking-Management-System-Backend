from fastapi.testclient import TestClient
def test_create_parking_spot(client: TestClient, auth_token:str):
    spot_data = {
        "level": 1,
        "section": "A",
        "spot_number": 1,
        "vehicle_type": "car",
        "exit_distance": 50,
        "short_term_only": False,
        "is_occupied":False,
    }

    headers = {"Authorization": auth_token}
    response = client.post("/parking_spots/", json=spot_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["level"] == spot_data["level"]
    assert data["spot_number"] == spot_data["spot_number"]

def test_get_parking_spots(client: TestClient, auth_token:str):
    headers = {"Authorization": auth_token}
    response = client.get("/parking_spots/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_parking_spot(client: TestClient, auth_token:str):
    headers = {"Authorization": auth_token}
    spot_data = {
        "level": 1,
        "section": "A",
        "spot_number": 2,
        "vehicle_type": "motorcycle",
        "exit_distance": 30,
        "short_term_only": True,
        "is_occupied":False,
    }
    response = client.put("/parking_spots/1", json=spot_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["spot_number"] == spot_data["spot_number"]

def test_delete_parking_spot(client: TestClient, auth_token:str):
    headers = {"Authorization": auth_token}
    response = client.delete("/parking_spots/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Parking spot deleted"}


def test_get_parking_spots_by_level(client: TestClient, auth_token:str):
    headers = {"Authorization": auth_token}
    response = client.get("/parking_spots/availability/level/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["level"] == 1

def test_get_parking_spots_by_section(client: TestClient, auth_token:str):
    headers = {"Authorization": auth_token}
    response = client.get("/parking_spots/availability/section/A", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["section"] == "A"

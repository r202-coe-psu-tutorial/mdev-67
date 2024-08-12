from fastapi.testclient import TestClient

from digimon.main import create_app

client = TestClient(create_app())


def get_merchants():
    response = client.get("/merchants")

    assert response.status_code == 200
    print(response.json())

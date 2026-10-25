import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def signed_in_client(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    app = create_app(database_url=database_url)

    with TestClient(app) as client:
        client.post(
            "/api/auth/register",
            json={
                "email": "anne@example.com",
                "password": "SecurePass123!",
            },
        )
        login_response = client.post(
            "/api/auth/login",
            json={
                "email": "anne@example.com",
                "password": "SecurePass123!",
            },
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        yield client, headers


@pytest.mark.parametrize("blank_field", ["make", "model", "category"])
def test_vehicle_text_fields_cannot_be_only_spaces(
    signed_in_client,
    blank_field,
):
    client, headers = signed_in_client
    vehicle = {
        "make": "Toyota",
        "model": "Corolla",
        "category": "Sedan",
        "price": "24999.99",
        "quantity": 2,
    }
    vehicle[blank_field] = "   "

    response = client.post(
        "/api/vehicles",
        headers=headers,
        json=vehicle,
    )
    inventory = client.get("/api/vehicles", headers=headers)

    assert response.status_code == 422
    assert inventory.json() == []
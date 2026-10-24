from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import create_app


def test_logged_in_user_can_update_a_vehicle(tmp_path):
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

        create_response = client.post(
            "/api/vehicles",
            headers=headers,
            json={
                "make": "Toyota",
                "model": "Corolla",
                "category": "Sedan",
                "price": "24999.99",
                "quantity": 3,
            },
        )
        assert create_response.status_code == 201
        vehicle_id = create_response.json()["id"]

        update_response = client.put(
            f"/api/vehicles/{vehicle_id}",
            headers=headers,
            json={
                "make": "Toyota",
                "model": "Corolla Hybrid",
                "category": "Hybrid",
                "price": "27999.99",
                "quantity": 5,
            },
        )
        list_response = client.get("/api/vehicles", headers=headers)

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["id"] == vehicle_id
    assert updated["model"] == "Corolla Hybrid"
    assert updated["category"] == "Hybrid"
    assert Decimal(str(updated["price"])) == Decimal("27999.99")
    assert updated["quantity"] == 5

    assert list_response.json()[0]["model"] == "Corolla Hybrid"
    assert list_response.json()[0]["quantity"] == 5
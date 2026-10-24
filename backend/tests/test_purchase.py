from fastapi.testclient import TestClient

from app.main import create_app


def test_purchase_reduces_stock_and_prevents_overselling(tmp_path):
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
                "make": "Honda",
                "model": "Civic",
                "category": "Sedan",
                "price": "23000.00",
                "quantity": 1,
            },
        )
        assert create_response.status_code == 201
        vehicle_id = create_response.json()["id"]

        first_purchase = client.post(
            f"/api/vehicles/{vehicle_id}/purchase",
            headers=headers,
        )
        second_purchase = client.post(
            f"/api/vehicles/{vehicle_id}/purchase",
            headers=headers,
        )
        inventory = client.get("/api/vehicles", headers=headers)

    assert first_purchase.status_code == 200
    assert first_purchase.json()["quantity"] == 0
    assert second_purchase.status_code == 409
    assert inventory.json()[0]["quantity"] == 0
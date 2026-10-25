from fastapi.testclient import TestClient

from app.main import create_app


def test_vehicle_make_cannot_be_only_spaces(tmp_path):
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

        response = client.post(
            "/api/vehicles",
            headers=headers,
            json={
                "make": "   ",
                "model": "Corolla",
                "category": "Sedan",
                "price": "24999.99",
                "quantity": 2,
            },
        )
        inventory = client.get("/api/vehicles", headers=headers)

    assert response.status_code == 422
    assert inventory.json() == []
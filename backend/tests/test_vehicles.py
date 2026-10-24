from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import create_app


def test_vehicle_list_requires_login(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    app = create_app(database_url=database_url)

    with TestClient(app) as client:
        response = client.get("/api/vehicles")

    assert response.status_code == 401


def test_logged_in_user_can_view_empty_vehicle_list(tmp_path):
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

        response = client.get(
            "/api/vehicles",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    assert response.json() == []


def test_logged_in_user_can_add_and_list_a_vehicle(tmp_path):
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
        list_response = client.get("/api/vehicles", headers=headers)

    assert create_response.status_code == 201
    created = create_response.json()
    assert isinstance(created["id"], int)
    assert created["make"] == "Toyota"
    assert created["model"] == "Corolla"
    assert created["category"] == "Sedan"
    assert Decimal(str(created["price"])) == Decimal("24999.99")
    assert created["quantity"] == 3

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["id"] == created["id"]
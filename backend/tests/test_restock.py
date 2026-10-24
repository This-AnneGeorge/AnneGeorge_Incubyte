from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, select

from app.main import User, create_app


def test_only_admin_can_restock_a_vehicle(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    app = create_app(database_url=database_url)

    with TestClient(app) as client:
        client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "password": "SecurePass123!",
            },
        )
        client.post(
            "/api/auth/register",
            json={
                "email": "admin@example.com",
                "password": "AdminPass123!",
            },
        )

        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
        )
        with Session(engine) as session:
            admin = session.exec(
                select(User).where(User.email == "admin@example.com")
            ).one()
            admin.role = "admin"
            session.add(admin)
            session.commit()

        user_login = client.post(
            "/api/auth/login",
            json={
                "email": "user@example.com",
                "password": "SecurePass123!",
            },
        )
        admin_login = client.post(
            "/api/auth/login",
            json={
                "email": "admin@example.com",
                "password": "AdminPass123!",
            },
        )
        user_headers = {
            "Authorization": f"Bearer {user_login.json()['access_token']}"
        }
        admin_headers = {
            "Authorization": f"Bearer {admin_login.json()['access_token']}"
        }

        create_response = client.post(
            "/api/vehicles",
            headers=user_headers,
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

        denied = client.post(
            f"/api/vehicles/{vehicle_id}/restock",
            headers=user_headers,
            json={"amount": 3},
        )
        restocked = client.post(
            f"/api/vehicles/{vehicle_id}/restock",
            headers=admin_headers,
            json={"amount": 3},
        )
        invalid_amount = client.post(
            f"/api/vehicles/{vehicle_id}/restock",
            headers=admin_headers,
            json={"amount": 0},
        )

    assert denied.status_code == 403
    assert restocked.status_code == 200
    assert restocked.json()["quantity"] == 4
    assert invalid_amount.status_code == 422
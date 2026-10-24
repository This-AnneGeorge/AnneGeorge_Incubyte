from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, select

from app.main import User, create_app


def test_only_admin_can_delete_a_vehicle(tmp_path):
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
                "make": "Toyota",
                "model": "Corolla",
                "category": "Sedan",
                "price": "24999.99",
                "quantity": 2,
            },
        )
        assert create_response.status_code == 201
        vehicle_id = create_response.json()["id"]

        denied = client.delete(
            f"/api/vehicles/{vehicle_id}",
            headers=user_headers,
        )
        deleted = client.delete(
            f"/api/vehicles/{vehicle_id}",
            headers=admin_headers,
        )
        inventory = client.get(
            "/api/vehicles",
            headers=admin_headers,
        )

    assert denied.status_code == 403
    assert deleted.status_code == 204
    assert inventory.json() == []
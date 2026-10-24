from fastapi.testclient import TestClient

from app.main import create_app


def test_register_creates_a_regular_user(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    app = create_app(database_url=database_url)

    with TestClient(app) as client:
        response = client.post(
            "/api/auth/register",
            json={
                "email": "anne@example.com",
                "password": "SecurePass123!",
            },
        )

    assert response.status_code == 201
    assert response.json()["email"] == "anne@example.com"
    assert response.json()["role"] == "user"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


def test_register_rejects_invalid_email(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    app = create_app(database_url=database_url)

    with TestClient(app) as client:
        response = client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "password": "SecurePass123!",
            },
        )

    assert response.status_code == 422
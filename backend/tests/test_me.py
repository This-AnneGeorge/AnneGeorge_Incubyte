from fastapi.testclient import TestClient

from app.main import create_app


def test_current_user_endpoint_returns_role(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    app = create_app(database_url=database_url)

    with TestClient(app) as client:
        unauthenticated = client.get("/api/auth/me")

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

        authenticated = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert unauthenticated.status_code == 401
    assert authenticated.status_code == 200
    assert authenticated.json()["email"] == "anne@example.com"
    assert authenticated.json()["role"] == "user"
    assert "password_hash" not in authenticated.json()
from fastapi.testclient import TestClient

from app.main import create_app


def test_search_filters_by_make_and_maximum_price(tmp_path):
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

        vehicles = [
            {
                "make": "Toyota",
                "model": "Corolla",
                "category": "Sedan",
                "price": "24999.99",
                "quantity": 3,
            },
            {
                "make": "Toyota",
                "model": "RAV4",
                "category": "SUV",
                "price": "35000.00",
                "quantity": 2,
            },
            {
                "make": "Honda",
                "model": "Civic",
                "category": "Sedan",
                "price": "23000.00",
                "quantity": 1,
            },
        ]

        for vehicle in vehicles:
            response = client.post(
                "/api/vehicles",
                headers=headers,
                json=vehicle,
            )
            assert response.status_code == 201

        response = client.get(
            "/api/vehicles/search",
            headers=headers,
            params={"make": "toyota", "max_price": "30000"},
        )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["model"] == "Corolla"
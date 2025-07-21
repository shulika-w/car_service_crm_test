"""Базові тести для Car Service CRM API."""


from fastapi.testclient import TestClient
from car_service_crm.main import app

def test_root():
    with TestClient(app) as client:
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json() == {"message": "API is working!"}

def test_register_and_login():
    import random
    email = f"test{random.randint(1,100000)}@example.com"
    password = "testpassword"

    with TestClient(app) as client:
        # Register
        reg = client.post("/users/register", json={
            "name": "Test",
            "email": email,
            "password": password
        })
        assert reg.status_code in (200, 201)
        assert reg.json()["email"] == email

        # Login
        login = client.post("/users/login", json={
            "email": email,
            "password": password
        })
        assert login.status_code == 200
        token = login.json()["access_token"]

        # Profile
        me = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200
        assert me.json()["email"] == email
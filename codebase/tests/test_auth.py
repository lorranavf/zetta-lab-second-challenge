from app.services.security import SecurityService


def test_login_success(auth_client, user_credentials):
    response = auth_client.post(
        "/login",
        data={
            "username": user_credentials["email"],
            "password": user_credentials["password"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure(auth_client, user_credentials):
    response = auth_client.post(
        "/login",
        data={"username": user_credentials["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_invalid_token(auth_client):
    auth_client.headers["Authorization"] = "Bearer invalidtoken"
    response = auth_client.get("/users")
    assert response.status_code == 401


def test_missing_user_id(auth_client):
    invalid_token = SecurityService.create_access_token(data={})
    auth_client.headers["Authorization"] = f"Bearer {invalid_token}"
    response = auth_client.get("/users")
    assert response.status_code == 401


def test_nonexistent_user(auth_client):
    fake_user_id = "00000000-0000-0000-0000-000000000000"
    invalid_token = SecurityService.create_access_token(data={"sub": fake_user_id})
    auth_client.headers["Authorization"] = f"Bearer {invalid_token}"
    response = auth_client.get("/users")
    assert response.status_code == 401

def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepass123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_username(client):
    client.post(
        "/auth/register",
        json={"username": "dup", "email": "dup1@example.com", "password": "pass"},
    )
    response = client.post(
        "/auth/register",
        json={"username": "dup", "email": "dup2@example.com", "password": "pass"},
    )
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={"username": "user1", "email": "same@example.com", "password": "pass"},
    )
    response = client.post(
        "/auth/register",
        json={"username": "user2", "email": "same@example.com", "password": "pass"},
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client, registered_user):
    response = client.post(
        "/auth/token",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, registered_user):
    response = client.post(
        "/auth/token",
        data={"username": registered_user["username"], "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/token",
        data={"username": "nobody", "password": "pass"},
    )
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/notes/")
    assert response.status_code == 401


def test_protected_route_with_invalid_token(client):
    response = client.get("/notes/", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401

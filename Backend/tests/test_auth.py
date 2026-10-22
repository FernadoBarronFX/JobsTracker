import jwt

def register(client, email="ana@mail.com", password="supersecreta1"):
    return client.post("/auth/register", json={"email": email, "password": password})


def test_login_success_returns_token(client):
    register(client)
    res = client.post(
        "/auth/login",
        data={"username": "ana@mail.com", "password": "supersecreta1"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password_fails(client):
    register(client)
    res = client.post(
        "/auth/login",
        data={"username": "ana@mail.com", "password": "incorrecta123"},
    )
    assert res.status_code == 401


def test_login_unknown_user_fails(client):
    res = client.post(
        "/auth/login",
        data={"username": "nadie@mail.com", "password": "supersecreta1"},
    )
    assert res.status_code == 401


def test_token_contains_user_id_and_expiration(client):
    user = register(client).json()
    token = client.post(
        "/auth/login",
        data={"username": "ana@mail.com", "password": "supersecreta1"},
    ).json()["access_token"]

    payload = jwt.decode(token, options={"verify_signature": False})
    assert payload["sub"] == str(user["id"])
    assert "exp" in payload




def test_register_user(client):
    res = client.post(
        "/auth/register",
        json={"email": "ana@mail.com", "password": "supersecreta1"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "ana@mail.com"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email_fails(client):
    body = {"email": "ana@mail.com", "password": "supersecreta1"}
    client.post("/auth/register", json=body)
    res = client.post("/auth/register", json=body)
    assert res.status_code == 409


def test_register_email_is_case_insensitive(client):
    client.post("/auth/register", json={"email": "ana@mail.com", "password": "supersecreta1"})
    res = client.post("/auth/register", json={"email": "ANA@mail.com", "password": "supersecreta1"})
    assert res.status_code == 409


def test_register_short_password_fails(client):
    res = client.post("/auth/register", json={"email": "ana@mail.com", "password": "123"})
    assert res.status_code == 422


def test_register_invalid_email_fails(client):
    res = client.post("/auth/register", json={"email": "no-es-un-correo", "password": "supersecreta1"})
    assert res.status_code == 422
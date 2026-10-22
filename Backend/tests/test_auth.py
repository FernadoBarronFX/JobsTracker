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
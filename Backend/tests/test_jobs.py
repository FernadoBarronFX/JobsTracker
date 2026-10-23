def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_create_job(auth_client):
    res = auth_client.post("/jobs", json={"company": "Acme", "title": "Fullstack Dev"})
    assert res.status_code == 201
    data = res.json()
    assert data["company"] == "Acme"
    assert data["status"] == "saved"
    assert "id" in data


def test_create_job_without_company_fails(auth_client):
    res = auth_client.post("/jobs", json={"title": "Fullstack Dev"})
    assert res.status_code == 422


def test_list_jobs(auth_client):
    auth_client.post("/jobs", json={"company": "A", "title": "Dev"})
    auth_client.post("/jobs", json={"company": "B", "title": "Dev"})
    res = auth_client.get("/jobs")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_filter_by_status(auth_client):
    auth_client.post("/jobs", json={"company": "A", "title": "Dev", "status": "applied"})
    auth_client.post("/jobs", json={"company": "B", "title": "Dev"})
    res = auth_client.get("/jobs?status=applied")
    assert len(res.json()) == 1
    assert res.json()[0]["company"] == "A"


def test_update_status(auth_client):
    job = auth_client.post("/jobs", json={"company": "A", "title": "Dev"}).json()
    res = auth_client.patch(f"/jobs/{job['id']}", json={"status": "interview"})
    assert res.status_code == 200
    assert res.json()["status"] == "interview"
    assert res.json()["company"] == "A"  # lo demás no cambió


def test_delete_job(auth_client):
    job = auth_client.post("/jobs", json={"company": "A", "title": "Dev"}).json()
    res = auth_client.delete(f"/jobs/{job['id']}")
    assert res.status_code == 204
    assert auth_client.get(f"/jobs/{job['id']}").status_code == 404


def test_get_missing_job_returns_404(auth_client):
    res = auth_client.get("/jobs/9999")
    assert res.status_code == 404
    
def test_jobs_require_authentication(client):
    assert client.get("/jobs").status_code == 401
    assert client.post("/jobs", json={"company": "A", "title": "Dev"}).status_code == 401


def test_invalid_token_is_rejected(client):
    res = client.get("/jobs", headers={"Authorization": "Bearer token-falso"})
    assert res.status_code == 401


def make_client_for(client, email):
    """Registra e inicia sesión con otro usuario, devolviendo sus encabezados."""
    client.post("/auth/register", json={"email": email, "password": "supersecreta1"})
    res = client.post("/auth/login", data={"username": email, "password": "supersecreta1"})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


def test_user_cannot_see_other_users_jobs(auth_client):
    auth_client.post("/jobs", json={"company": "Secreta", "title": "Dev"})
    otro = make_client_for(auth_client, "beto@mail.com")

    res = auth_client.get("/jobs", headers=otro)
    assert res.json() == []


def test_user_cannot_modify_or_delete_other_users_jobs(auth_client):
    job = auth_client.post("/jobs", json={"company": "Secreta", "title": "Dev"}).json()
    otro = make_client_for(auth_client, "beto@mail.com")

    assert auth_client.get(f"/jobs/{job['id']}", headers=otro).status_code == 404
    assert auth_client.patch(f"/jobs/{job['id']}", json={"status": "offer"}, headers=otro).status_code == 404
    assert auth_client.delete(f"/jobs/{job['id']}", headers=otro).status_code == 404

    # y la vacante sigue intacta para su dueña
    assert auth_client.get(f"/jobs/{job['id']}").status_code == 200
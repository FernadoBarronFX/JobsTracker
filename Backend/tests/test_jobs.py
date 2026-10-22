def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_create_job(client):
    res = client.post("/jobs", json={"company": "Acme", "title": "Fullstack Dev"})
    assert res.status_code == 201
    data = res.json()
    assert data["company"] == "Acme"
    assert data["status"] == "saved"
    assert "id" in data


def test_create_job_without_company_fails(client):
    res = client.post("/jobs", json={"title": "Fullstack Dev"})
    assert res.status_code == 422


def test_list_jobs(client):
    client.post("/jobs", json={"company": "A", "title": "Dev"})
    client.post("/jobs", json={"company": "B", "title": "Dev"})
    res = client.get("/jobs")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_filter_by_status(client):
    client.post("/jobs", json={"company": "A", "title": "Dev", "status": "applied"})
    client.post("/jobs", json={"company": "B", "title": "Dev"})
    res = client.get("/jobs?status=applied")
    assert len(res.json()) == 1
    assert res.json()[0]["company"] == "A"


def test_update_status(client):
    job = client.post("/jobs", json={"company": "A", "title": "Dev"}).json()
    res = client.patch(f"/jobs/{job['id']}", json={"status": "interview"})
    assert res.status_code == 200
    assert res.json()["status"] == "interview"
    assert res.json()["company"] == "A"  # lo demás no cambió


def test_delete_job(client):
    job = client.post("/jobs", json={"company": "A", "title": "Dev"}).json()
    res = client.delete(f"/jobs/{job['id']}")
    assert res.status_code == 204
    assert client.get(f"/jobs/{job['id']}").status_code == 404


def test_get_missing_job_returns_404(client):
    res = client.get("/jobs/9999")
    assert res.status_code == 404
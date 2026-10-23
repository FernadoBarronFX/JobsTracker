import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
import os
os.environ.setdefault("SECRET_KEY", "clave-solo-para-pruebas")
from main import app

# Base de datos en memoria, solo para pruebas
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, autoflush=False)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)  # tablas nuevas antes de cada prueba

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)  # se borran al terminar
    
    
@pytest.fixture()
def auth_client(client):
    """Cliente ya autenticado como ana@mail.com."""
    client.post("/auth/register", json={"email": "ana@mail.com", "password": "supersecreta1"})
    res = client.post("/auth/login", data={"username": "ana@mail.com", "password": "supersecreta1"})
    client.headers["Authorization"] = f"Bearer {res.json()['access_token']}"
    return client
    
    
    
    
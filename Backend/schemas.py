from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from models import JobStatus

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class JobCreate(BaseModel):
    company: str
    title: str
    url: str | None = None
    location: str | None = None
    modality: str | None = None
    salary: str | None = None
    status: JobStatus = JobStatus.saved

class JobUpdate(BaseModel):
    """Todos los campos opcionales: sirve para actualizaciones parciales."""
    company: str | None = None
    title: str | None = None
    url: str | None = None
    location: str | None = None
    modality: str | None = None
    salary: str | None = None
    status: JobStatus | None = None


class JobOut(JobCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
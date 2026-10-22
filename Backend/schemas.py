from datetime import datetime
from pydantic import BaseModel, ConfigDict
from models import JobStatus

class JobCreate(BaseModel):
    company: str
    title: str
    url: str | None = None
    location: str | None = None
    modality: str | None = None
    salary: str | None = None
    description: str | None = None
    notes: str | None = None
    status: JobStatus = JobStatus.saved
    contact_email: str | None = None

class JobUpdate(BaseModel):
    """Todos los campos opcionales: sirve para actualizaciones parciales."""
    company: str | None = None
    title: str | None = None
    url: str | None = None
    location: str | None = None
    modality: str | None = None
    salary: str | None = None
    description: str | None = None
    notes: str | None = None
    status: JobStatus | None = None
    contact_email: str | None = None


class JobOut(JobCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
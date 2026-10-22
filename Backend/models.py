import enum

from datetime import datetime
from sqlalchemy import DateTime, Enum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class JobStatus(str, enum.Enum):
    saved = "saved"
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(120))
    title: Mapped[str] = mapped_column(String(160))
    url: Mapped[str | None] = mapped_column(String(500), default=None)
    location: Mapped[str | None] = mapped_column(String(120), default=None)
    modality: Mapped[str | None] = mapped_column(String(30), default=None)  
    salary: Mapped[str | None] = mapped_column(String(80), default=None)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    notes: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.saved)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
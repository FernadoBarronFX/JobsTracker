from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobsTaracker")

@app.get("/health")
def health():
    return {"status" : "ok"}



@app.post("/jobs", response_model=schemas.JobOut, status_code=201)
def create_job(data:schemas.JobCreate, db:Session = Depends(get_db)):
    job = models.Job(**data.model_dump())
    db.add (job)
    db.commit()
    db.refresh(job)
    return job



@app.get("/jobs" , response_model=list[schemas.JobOut])
def list_jobs(status:models.JobStatus | None = None, db:Session = Depends(get_db)):
    query = select(models.Job).order_by(models.Job.created_at.desc())
    if status:
        query = query.where(models.Job.status == status)
    return db.scalars(query).all()



@app.get("/jobs/{job_id}", response_model=schemas.JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(models.Job, job_id)
    if not job:
        raise HTTPException(404, "Vacante no encontrada")
    return job



@app.patch("/jobs/{job_id}", response_model=schemas.JobOut)
def update_job(job_id: int, data: schemas.JobUpdate, db: Session = Depends(get_db)):
    job = db.get(models.Job, job_id)
    if not job:
        raise HTTPException(404, "Vacante no encontrada")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job



@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(models.Job, job_id)
    if not job:
        raise HTTPException(404, "Vacante no encontrada")
    db.delete(job)
    db.commit()
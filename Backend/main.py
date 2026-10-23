from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from security import create_access_token, hash_password, verify_password
from deps import get_current_user
import os 

import models
import schemas
from database import get_db


app = FastAPI(title="JobsTaracker")

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status" : "ok"}



@app.post("/auth/login", response_model=schemas.Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    
    email = form.username.lower()
    user = db.scalar(select(models.User).where(models.User.email == email))

    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return schemas.Token(access_token=create_access_token(user.id))



@app.post("/auth/register", response_model=schemas.UserOut, status_code=201)
def register(data:schemas.UserCreate, db:Session = Depends(get_db)):
    email = data.email.lower()
    
    existing = db.scalar(select(models.User).where(models.User.email == email))
    if existing:
        raise HTTPException(409, "Correo ya registrado")

    user = models.User(email=email,hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



@app.post("/jobs", response_model=schemas.JobOut, status_code=201)
def create_job(
    data: schemas.JobCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    job = models.Job(**data.model_dump(), user_id=user.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job



@app.get("/jobs", response_model=list[schemas.JobOut])
def list_jobs(
    status: models.JobStatus | None = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    query = (
        select(models.Job)
        .where(models.Job.user_id == user.id)
        .order_by(models.Job.created_at.desc())
    )
    if status:
        query = query.where(models.Job.status == status)
    return db.scalars(query).all()



def get_user_job(job_id: int, db: Session, user: models.User) -> models.Job:
    """Busca una vacante que pertenezca al usuario; si no, 404."""
    job = db.get(models.Job, job_id)
    if not job or job.user_id != user.id:
        raise HTTPException(404, "Vacante no encontrada")
    return job



@app.get("/jobs/{job_id}", response_model=schemas.JobOut)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    return get_user_job(job_id, db, user)



@app.patch("/jobs/{job_id}", response_model=schemas.JobOut)
def update_job(
    job_id: int,
    data: schemas.JobUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    job = get_user_job(job_id, db, user)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job


@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    job = get_user_job(job_id, db, user)
    db.delete(job)
    db.commit()
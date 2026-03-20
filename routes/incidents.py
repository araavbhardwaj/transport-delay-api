from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

router = APIRouter(prefix="/incidents", tags=["Incidents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
    db_incident = models.Incident(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Incident).all()

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).get(id)
    db.delete(incident)
    db.commit()
    return {"message": "Deleted"}
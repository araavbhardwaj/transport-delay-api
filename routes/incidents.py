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

    if not incident:
        return {"error": "Not found"}

    db.delete(incident)
    db.commit()
    return {"message": "Deleted"}

@router.put("/{id}")
def update_incident(id: int, updated: schemas.IncidentCreate, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).get(id)

    if not incident:
        return {"error": "Incident not found"}

    incident.location = updated.location
    incident.route = updated.route
    incident.delay_minutes = updated.delay_minutes
    incident.description = updated.description

    db.commit()
    return {"message": "Updated successfully"}
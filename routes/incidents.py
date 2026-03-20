from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from auth import verify_token
import models, schemas

router = APIRouter(prefix="/incidents", tags=["Incidents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE (Protected)
@router.post("/")
def create_incident(
    incident: schemas.IncidentCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    db_incident = models.Incident(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

# READ (Public)
@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Incident).all()

# UPDATE (Protected)
@router.put("/{id}")
def update_incident(
    id: int,
    updated: schemas.IncidentCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    incident = db.query(models.Incident).get(id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    incident.location = updated.location
    incident.route = updated.route
    incident.delay_minutes = updated.delay_minutes
    incident.description = updated.description

    db.commit()

    return {"message": "Updated successfully"}

# DELETE (Protected)
@router.delete("/{id}")
def delete_incident(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    incident = db.query(models.Incident).get(id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    db.delete(incident)
    db.commit()

    return {"message": "Deleted successfully"}
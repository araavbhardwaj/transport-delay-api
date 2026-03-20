from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_db():
    db = SessionLocal()
    yield db
    db.close()

@router.get("/average-delay")
def average_delay(db: Session = Depends(get_db)):
    incidents = db.query(models.Incident).all()
    if not incidents:
        return {"average_delay": 0}

    avg = sum(i.delay_minutes for i in incidents) / len(incidents)
    return {"average_delay": avg}
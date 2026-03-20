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

@router.get("/delay-by-route")
def delay_by_route(db: Session = Depends(get_db)):
    incidents = db.query(models.Incident).all()

    data = {}
    for i in incidents:
        if i.route not in data:
            data[i.route] = []
        data[i.route].append(i.delay_minutes)

    result = {
        route: sum(vals)/len(vals)
        for route, vals in data.items()
    }

    return result
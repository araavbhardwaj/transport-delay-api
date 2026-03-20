from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from database import SessionLocal
import models

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/hotspots")
def get_traffic_hotspots(db: Session = Depends(get_db)):
    """Identifies locations with the highest total delay minutes."""
    hotspots = db.query(
        models.Incident.location,
        func.count(models.Incident.id).label("total_incidents"),
        func.sum(models.Incident.delay_minutes).label("total_delay_minutes"),
        func.avg(models.Incident.delay_minutes).label("average_delay")
    ).group_by(models.Incident.location).order_by(func.sum(models.Incident.delay_minutes).desc()).limit(5).all()

    return [
        {
            "location": h.location, 
            "total_incidents": h.total_incidents, 
            "total_delay_minutes": h.total_delay_minutes, 
            "average_delay": round(h.average_delay, 2) if h.average_delay else 0
        } 
        for h in hotspots
    ]

@router.get("/route/{route_name}")
def get_route_performance(route_name: str, db: Session = Depends(get_db)):
    """Provides deep analytics for a specific route."""
    stats = db.query(
        func.count(models.Incident.id).label("incident_count"),
        func.avg(models.Incident.delay_minutes).label("avg_delay"),
        func.max(models.Incident.delay_minutes).label("max_delay")
    ).filter(models.Incident.route == route_name).first()

    if not stats.incident_count:
        return {"message": "No data found for this route."}

    return {
        "route": route_name,
        "total_incidents": stats.incident_count,
        "average_delay_minutes": round(stats.avg_delay, 2) if stats.avg_delay else 0,
        "maximum_delay_minutes": stats.max_delay
    }

@router.get("/trends/recent")
def get_recent_trends(days: int = Query(7, description="Number of days to look back"), db: Session = Depends(get_db)):
    """Analyzes delays over the last X days to find temporal patterns."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    recent_incidents = db.query(models.Incident).filter(models.Incident.timestamp >= cutoff_date).all()
    
    if not recent_incidents:
        return {"message": f"No incidents in the last {days} days."}
        
    total_delay = sum(i.delay_minutes for i in recent_incidents)
    
    return {
        "timeframe_days": days,
        "incident_count": len(recent_incidents),
        "total_delay_minutes": total_delay,
        "average_daily_delay": round(total_delay / days, 2) if days > 0 else total_delay
    }
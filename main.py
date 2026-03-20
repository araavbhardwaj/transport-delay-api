from fastapi import FastAPI
from routes import incidents, analytics, users
from database import Base, engine
import models

# CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transport Delay Analytics API")

app.include_router(incidents.router)
app.include_router(analytics.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API running"}
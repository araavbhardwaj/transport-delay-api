from pydantic import BaseModel, ConfigDict
import datetime

class IncidentCreate(BaseModel):
    location: str
    route: str
    delay_minutes: int
    description: str

class IncidentResponse(IncidentCreate):
    id: int
    timestamp: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    password: str
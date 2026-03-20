from pydantic import BaseModel
import datetime

class IncidentCreate(BaseModel):
    location: str
    route: str
    delay_minutes: int
    description: str

class IncidentResponse(IncidentCreate):
    id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str
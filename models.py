from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    route = Column(String)
    delay_minutes = Column(Integer)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
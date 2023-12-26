from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from datetime import datetime

DATABASE_URL = "postgresql://postgres:Josiah1!@localhost/django"

database = Database(DATABASE_URL)
metadata = declarative_base()

class RawData(metadata):
    __tablename__ = "raw_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(Integer)
    hdop = Column(Float)
    altitude = Column(Float)
    speed = Column(Float)
    raw_data = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class RawDataCreate(BaseModel):
    device_id: int
    latitude: float
    longitude: float
    timestamp: int
    hdop: float
    altitude: float
    speed: float
    raw_data: str

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

@app.post("/mobile_capture/")
async def create_raw_data(raw_data: RawDataCreate):
    query = RawData.__table__.insert().values(**raw_data.dict())
    await database.execute(query)
    return {"status": "Record inserted successfully"}

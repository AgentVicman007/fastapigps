from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer, String, DateTime, text
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
    device_id = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(Integer)
    hdop = Column(String)
    altitude = Column(Float)
    speed = Column(Float)
    raw_data = Column(String)
    created_at = Column(DateTime, server_default=text("(now() at time zone 'UTC')"))

class RawDataCreate(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    timestamp: int
    hdop: str
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

@app.post("/capture_raw_data2")
async def capture_raw_data2(raw_data: RawDataCreate):
    print(raw_data.dict())  # Add this line to print the received data

    # Assuming you have a database logic to insert the raw_data into your PostgreSQL database
    # Replace the following lines with your actual database insertion logic
    db_raw_data = RawData(**raw_data.dict())
    query = RawData.__table__.insert().values(**db_raw_data.__dict__)
    await database.execute(query)
    
    response_data = {
        "status": "Record inserted successfully",
        "device_id": raw_data.device_id,
        "latitude": raw_data.latitude,
        "longitude": raw_data.longitude,
        "timestamp": raw_data.timestamp,
        "hdop": raw_data.hdop,
        "altitude": raw_data.altitude,
        "speed": raw_data.speed,
        "raw_data": raw_data.raw_data,
    }
    return response_data

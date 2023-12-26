from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Replace 'your_postgres_connection_string' with your actual PostgreSQL connection string
DATABASE_URL = "postgresql://postgres:Josiah1!@localhost/django"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class RawData(Base):
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

Base.metadata.create_all(bind=engine)

app = FastAPI()

class MobileCapture(BaseModel):
    id: int
    timestamp: int
    lat: float
    lon: float
    speed: float
    bearing: float
    altitude: float
    accuracy: float
    batt: float

@app.post("/mobile_capture/")
async def create_mobile_capture(mobile_capture: MobileCapture):
    db_mobile_capture = RawData(
        device_id=mobile_capture.id,
        latitude=mobile_capture.lat,
        longitude=mobile_capture.lon,
        timestamp=mobile_capture.timestamp,
        hdop=mobile_capture.accuracy,
        altitude=mobile_capture.altitude,
        speed=mobile_capture.speed,
        raw_data=f"Some raw data string"  # You can customize this field based on your requirements
    )
    db = SessionLocal()
    db.add(db_mobile_capture)
    db.commit()
    db.refresh(db_mobile_capture)
    db.close()
    return db_mobile_capture

# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy.orm import Session
# from models import Base, RawData
# from database import SessionLocal, engine
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from models import Base, RawData
from database import SessionLocal, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RawDataRequest(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    timestamp: int
    hdop: str
    altitude: float
    speed: float
    raw_data: str

@app.post("/capture_raw_data")
def capture_raw_data(data: RawDataRequest, db: Session = Depends(get_db)):
    raw_data_entry = RawData(**data.dict())
    db.add(raw_data_entry)
    db.commit()
    db.refresh(raw_data_entry)
    return {"status": "success", "id": raw_data_entry.id}






@app.get("/capture_raw_data2")
def capture_raw_data2(
    id: str = Query(None, alias="id"),
    lat: float = Query(None, alias="lat"),
    lon: float = Query(None, alias="lon"),
    db: Session = Depends(get_db)
):
    raw_data_entry = RawData(
        device_id=id,
        latitude=lat,
        longitude=lon,
        # Fill in other fields as None or with default values if necessary
    )
    db.add(raw_data_entry)
    db.commit()
    db.refresh(raw_data_entry)
    return {"status": "success", "id": raw_data_entry.id}

    
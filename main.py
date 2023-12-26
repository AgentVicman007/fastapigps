from fastapi import FastAPI, HTTPException, Depends, Query, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from typing import List
from database import SessionLocal  # Changed to absolute import
from models import RawData, Address  # Changed to absolute impor
import googlemaps
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware # once in prod we need to remove
# Initialize FastAPI app
app = FastAPI()

# List of allowed origins (use ["*"] for allowing all origins) ONCE IN PROD might need to remove
origins = [
    "http://localhost:3000",  # Adjust with your front-end URL
    "http://localhost:8000",
    "http://64.227.106.200:800"
    # Add more origins as needed
]

# Add CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # List of allowed origins
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Google Maps client with your API key
gmaps = googlemaps.Client(key='AIzaSyAm4yG78grfnhz4QoGZQbJzQRHgUKoiU8E')

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class RawDataRequest(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    timestamp: int
    hdop: str
    altitude: float
    speed: float
    raw_data: str

class DeviceQuery(BaseModel):
    device_ids: List[str] = Field(..., description="List of device IDs")

class AddressIn(BaseModel):
    added_by: str
    client_id: int
    full_address: str
    service_rep: str
    email: EmailStr
    mobile: str
    updated_by: str = None
    alert: bool = Field(default=False, description="Alert flag, defaults to No if left blank")
    radius: int = Field(..., ge=1, le=25, description="Radius between 1 and 25, digits only")

# Function to get coordinates
def get_coordinates(address):
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            return None, None
    except Exception as e:
        print(f"Error in geocoding: {e}")
        return None, None

@app.post("/addresses/")
async def create_address(address: AddressIn, db: Session = Depends(get_db)):

    try:
        latitude, longitude = get_coordinates(address.full_address)
        if latitude is None or longitude is None:
            raise HTTPException(status_code=400, detail="Could not geocode address")

        new_address = Address(
            added_by=address.added_by,
            client_id=address.client_id,
            full_address=address.full_address,
            service_rep=address.service_rep,
            email=address.email,
            mobile=address.mobile,
            updated_by=address.updated_by,
            updated_date=datetime.utcnow() if address.updated_by else None,
            alert=address.alert,
            radius=address.radius,
            latitude=latitude,
            longitude=longitude

        )

        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        return new_address
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

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
    )
    db.add(raw_data_entry)
    db.commit()
    db.refresh(raw_data_entry)
    return {"status": "success", "id": raw_data_entry.id}

@app.post("/get_latest_data")
def get_latest_data(query: DeviceQuery, db: Session = Depends(get_db)):
    latest_data = []
    for device_id in query.device_ids:
        latest_entry = db.query(RawData).filter(RawData.device_id == device_id).order_by(RawData.created_at.desc()).first()
        if latest_entry:
            latest_data.append({
                "device_id": latest_entry.device_id,
                "latitude": latest_entry.latitude,
                "longitude": latest_entry.longitude,
                "timestamp": latest_entry.timestamp,
                "hdop": latest_entry.hdop,
                "altitude": latest_entry.altitude,
                "speed": latest_entry.speed,
                "raw_data": latest_entry.raw_data,
                "created_at": latest_entry.created_at
            })
    return latest_data

@app.get("/mobile_capture/")
async def mobile_capture(
    id: str, 
    lat: float, 
    lon: float, 
    timestamp: int, 
    hdop: str, 
    altitude: float, 
    speed: float, 
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        raw_data = RawData(
            device_id=id,
            latitude=lat,
            longitude=lon,
            timestamp=timestamp,
            hdop=hdop,
            altitude=altitude,
            speed=speed,
            raw_data=str(request.query_params)
        )

        db.add(raw_data)
        db.commit()
        return {"message": "Data saved successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException

app = FastAPI()

# Single endpoint to capture payload from either URL parameters or JSON data
@app.post("/capture_payload")
async def capture_payload(id: int = None, timestamp: int = None, lat: float = None, lon: float = None,
                          speed: float = None, bearing: float = None, altitude: float = None,
                          accuracy: float = None, batt: int = None, raw_payload: str = None):
    if raw_payload is not None:
        # Payload from raw data
        print("Raw Payload received:", raw_payload)
        return {"message": "Raw Payload captured successfully", "payload": raw_payload}
    elif any(arg is None for arg in [id, timestamp, lat, lon, speed, bearing, altitude, accuracy, batt]):
        # Check for missing parameters
        raise HTTPException(status_code=400, detail="Invalid payload format")
    else:
        # Payload from URL parameters
        payload = {"id": id, "timestamp": timestamp, "lat": lat, "lon": lon,
                   "speed": speed, "bearing": bearing, "altitude": altitude,
                   "accuracy": accuracy, "batt": batt}
        print("Payload received:", payload)
        return {"message": "Payload captured successfully", "payload": payload}

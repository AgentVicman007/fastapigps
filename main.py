from fastapi import FastAPI, HTTPException

app = FastAPI()

# Endpoint to capture payload from URL parameters
@app.get("/capture_payload")
async def capture_payload_from_params(param1: str, param2: int):
    payload = {"param1": param1, "param2": param2}
    print("Payload received:", payload)
    return {"message": "Payload captured successfully", "payload": payload}

# Endpoint to capture payload from JSON data
@app.post("/capture_payload_json")
async def capture_payload_from_json(data: dict):
    print("Payload received:", data)
    return {"message": "Payload captured successfully", "payload": data}

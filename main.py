from fastapi import FastAPI, HTTPException

app = FastAPI()

# Single endpoint to capture payload from either URL parameters or JSON data
@app.post("/capture_payload")
async def capture_payload(data: dict = None, param1: str = None, param2: int = None):
    if data is not None:
        # Payload from JSON data
        payload = data
    elif param1 is not None and param2 is not None:
        # Payload from URL parameters
        payload = {"param1": param1, "param2": param2}
    else:
        raise HTTPException(status_code=400, detail="Invalid payload format")

    print("Payload received:", payload)
    return {"message": "Payload captured successfully", "payload": payload}

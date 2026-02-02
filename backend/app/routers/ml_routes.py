from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services.model_inference import model_service

router = APIRouter(prefix="/ml", tags=["ML Operations"])

class PredictRequest(BaseModel):
    vehicle_count: int
    avg_speed: float
    humidity: float
    temperature: float
    weather: str
    vehicle_type: str

@router.get("/predict")
def predict_get(
    vehicle_count: int = 250,
    speed: float = 30.0,
    weather: str = "Clear"
):
    """
    GET endpoint as requested: /predict?vehicle_count=250&speed=30&weather=Clear
    """
    # Map query params to features
    features = {
        "vehicle_count": vehicle_count,
        "avg_speed": speed,
        "weather": weather,
        "humidity": 50.0, # default
        "temperature": 25.0, # default
        "vehicle_type": "Car" # default
    }
    
    pred = model_service.predict(features)
    return {"predicted_co2_g_per_km": round(pred, 2)}

@router.post("/predict")
def predict_post(req: PredictRequest):
    features = req.dict()
    pred = model_service.predict(features)
    return {"predicted_co2_g_per_km": round(pred, 2)}

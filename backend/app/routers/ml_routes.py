from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os

router = APIRouter(prefix="/ml", tags=["ML Operations"])

# matches your docker-compose service and port
ML_WORKER_URL = os.getenv("ML_WORKER_URL", "http://ml_worker:9000")


# ---------- Request Models ----------
class RetrainRequest(BaseModel):
    model_type: str = "rf"   # or "lr"

class PredictRequest(BaseModel):
    features: dict           # example: {"temperature": 25, "distance": 5.3}


# ---------- Routes ----------
@router.post("/retrain")
def retrain(req: RetrainRequest):
    """
    Trigger model retraining via ML Worker.
    """
    try:
        response = requests.post(
            f"{ML_WORKER_URL}/train",
            json=req.dict(),
            timeout=180
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Retraining request failed: {str(e)}")


@router.post("/predict")
def predict(req: PredictRequest):
    """
    Forward prediction request to ML Worker.
    """
    try:
        response = requests.post(
            f"{ML_WORKER_URL}/predict",
            json=req.dict(),
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Prediction request failed: {str(e)}")

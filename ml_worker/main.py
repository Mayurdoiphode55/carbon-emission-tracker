from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import os
import joblib
from pathlib import Path
from pipeline.train_pipeline import run_training_pipeline, MODEL_SAVE_DIR

app = FastAPI(title="ML Worker Service")

# ============================================================
# Request models
# ============================================================
class TrainRequest(BaseModel):
    model_type: str = "rf"  # "rf" or "lr"

class PredictRequest(BaseModel):
    features: dict  # e.g. {"temperature": 21.5, "vehicle_type": 2, "fuel_used": 10.3}


# ============================================================
# Health check
# ============================================================
@app.get("/")
def root():
    return {"status": "ok", "message": "ML Worker running"}


# ============================================================
# Train endpoint
# ============================================================
@app.post("/train")
def train_model(req: TrainRequest):
    try:
        summary = run_training_pipeline(model_type=req.model_type)
        return {"status": "success", "summary": summary}
    except Exception as e:
        import traceback
        print("=== TRAIN PIPELINE ERROR ===")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# ============================================================
# Predict endpoint
# ============================================================
@app.post("/predict")
def predict(req: PredictRequest):
    """
    Load latest trained model and make prediction for given features.
    """
    model_dir = Path(MODEL_SAVE_DIR)
    if not model_dir.exists():
        raise HTTPException(status_code=404, detail="No model directory found")

    # Get the latest model file by modification time
    model_files = sorted(model_dir.glob("*.joblib"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not model_files:
        raise HTTPException(status_code=404, detail="No trained models available")

    latest_model_path = model_files[0]
    model_obj = joblib.load(str(latest_model_path))
    model = model_obj["model"]
    features = model_obj["features"]

    # Prepare feature vector
    input_vector = [req.features.get(f, 0) for f in features]
    prediction = model.predict([input_vector])[0]

    return {
        "prediction": float(prediction),
        "model_path": str(latest_model_path),
        "features_used": features
    }

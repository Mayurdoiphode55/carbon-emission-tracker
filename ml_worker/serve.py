from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import mlflow
import mlflow.sklearn
import os
import pandas as pd
from train import train_and_log

app = FastAPI(title="ML Worker Service")

MLFLOW_URI = os.getenv("MLFLOW_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_URI)
EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT", "carbon_emission_models")

# ------------------- Load model -------------------
@app.on_event("startup")
def load_model():
    global model
    client = mlflow.tracking.MlflowClient()
    exp = client.get_experiment_by_name(EXPERIMENT_NAME)
    runs = client.search_runs(exp.experiment_id, order_by=["attributes.start_time DESC"], max_results=1)
    if runs:
        model_uri = f"runs:/{runs[0].info.run_id}/model"
        model = mlflow.sklearn.load_model(model_uri)
    else:
        model = None

class PredictRequest(BaseModel):
    features: dict

@app.post("/predict")
def predict(req: PredictRequest):
    if model is None:
        return {"error": "No trained model available."}
    x = pd.DataFrame([req.features])
    pred = model.predict(x)
    return {"prediction": pred.tolist()}

@app.post("/train")
def train_now():
    result = train_and_log()
    return {"status": "completed", "metrics": result}

@app.post("/train-async")
def train_async(background_tasks: BackgroundTasks):
    background_tasks.add_task(train_and_log)
    return {"status": "scheduled"}

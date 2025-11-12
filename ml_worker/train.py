import os
import requests
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import mlflow
import mlflow.sklearn
from pymongo import MongoClient
from datetime import datetime

# ------------------- Configuration -------------------
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
MLFLOW_URI = os.getenv("MLFLOW_URI", "http://mlflow:5000")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT", "carbon_emission_models")

mlflow.set_tracking_uri(MLFLOW_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["carbon_tracker"]
runs_col = db["ml_runs"]

# ------------------- Data Fetch -------------------
def fetch_live_data():
    """Fetch latest analytics data from backend."""
    resp = requests.get(f"{BACKEND_URL}/analytics/avg_speed_by_road")
    resp.raise_for_status()
    data = resp.json()["results"]

    df = pd.DataFrame(data)
    if df.empty:
        raise ValueError("No data received from backend analytics API.")
    # assume numeric column target is avg_speed or emission
    df = df.rename(columns={"avg_speed": "target"})
    return df

# ------------------- Pipeline -------------------
def preprocess(df):
    df = df.dropna()
    X = df.drop(columns=["target"])
    y = df["target"]
    return X, y

def train_and_log():
    df = fetch_live_data()
    X, y = preprocess(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run() as run:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        mlflow.log_metric("mse", float(mse))
        mlflow.log_metric("r2", float(r2))
        mlflow.sklearn.log_model(model, "model")

        model_path = f"/tmp/model_{run.info.run_id}.joblib"
        joblib.dump(model, model_path)
        mlflow.log_artifact(model_path, artifact_path="local_models")

        runs_col.insert_one({
            "run_id": run.info.run_id,
            "timestamp": datetime.utcnow(),
            "mse": float(mse),
            "r2": float(r2),
            "artifact_uri": run.info.artifact_uri,
            "status": "completed"
        })

        return {
            "run_id": run.info.run_id,
            "mse": mse,
            "r2": r2,
            "artifact_uri": run.info.artifact_uri
        }

if __name__ == "__main__":
    print("🚀 Starting ML training job...")
    result = train_and_log()
    print("✅ Training complete:", result)

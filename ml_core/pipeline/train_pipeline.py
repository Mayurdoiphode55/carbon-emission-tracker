import os
import time
import json
from datetime import datetime
from typing import Tuple

import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import mlflow
import mlflow.sklearn

# Optional DB clients
from pymongo import MongoClient
from sqlalchemy import create_engine, text


# ============================================================
# Environment Configuration (matches docker-compose.yml)
# ============================================================
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "carbon-emission-baselines")
MODEL_SAVE_DIR = os.getenv("MODEL_SAVE_DIR", "/app/models")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/ml_models")
POSTGRES_DSN = os.getenv("POSTGRES_DSN", "postgresql://carbon_user:carbon_pass@postgres:5432/carbon_db")

os.makedirs(MODEL_SAVE_DIR, exist_ok=True)


# ============================================================
# MLflow configuration
# ============================================================
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Ensure experiment exists
exp = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)
if exp is None:
    exp_id = mlflow.create_experiment(MLFLOW_EXPERIMENT_NAME)
else:
    exp_id = exp.experiment_id

mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)


# ============================================================
# Step 1: Fetch live analytics data from backend API
# ============================================================
def fetch_analytics_data() -> pd.DataFrame:
    url = f"{BACKEND_URL}/analytics/data"
    print(f"Fetching data from: {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return pd.DataFrame(data)


# ============================================================
# Step 2: Preprocessing
# ============================================================
def preprocess(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    df = df.copy()
    if "emissions" not in df.columns:
        raise ValueError("Expected column 'emissions' in dataset")

    df = df.dropna(subset=["emissions"])
    y = df["emissions"].astype(float)
    X = df.drop(columns=["emissions", "id"], errors="ignore")

    for col in X.select_dtypes(include=[np.number]).columns:
        X[col] = X[col].fillna(X[col].median())

    cat_cols = X.select_dtypes(include=["object", "category"]).columns
    if len(cat_cols) > 0:
        X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

    return X, y


# ============================================================
# Step 3: Train + Evaluate model
# ============================================================
def train_and_evaluate(X: pd.DataFrame, y: pd.Series, model_type="rf", random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

    if model_type == "lr":
        model = LinearRegression()
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=random_state, n_jobs=-1)

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mse = mean_squared_error(y_test, preds)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, preds)

    metrics = {"mse": float(mse), "rmse": float(rmse), "r2": float(r2)}
    return model, metrics, X_test, y_test, preds


# ============================================================
# Step 4: Save model locally
# ============================================================
def save_model_local(model, features: list, model_name=None):
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    model_name = model_name or f"model_{ts}.joblib"
    path = os.path.join(MODEL_SAVE_DIR, model_name)
    joblib.dump({"model": model, "features": features}, path)
    return path


# ============================================================
# Step 5: Record metadata (optional)
# ============================================================
def record_metadata_mongo(path, metrics, params):
    try:
        client = MongoClient(MONGO_URI)
        db = client.get_database("ml_models")
        coll = db["models"]
        doc = {
            "path": path,
            "metrics": metrics,
            "params": params,
            "created_at": datetime.utcnow(),
        }
        res = coll.insert_one(doc)
        return str(res.inserted_id)
    except Exception as e:
        print(f"[MongoDB] Failed to save metadata: {e}")
        return None


def record_metadata_postgres(path, metrics, params):
    try:
        engine = create_engine(POSTGRES_DSN)
        with engine.begin() as conn:
            conn.execute(
                text("""
                    CREATE TABLE IF NOT EXISTS ml_models (
                        id SERIAL PRIMARY KEY,
                        path TEXT,
                        params JSONB,
                        metrics JSONB,
                        created_at TIMESTAMP
                    )
                """)
            )
            res = conn.execute(
                text(
                    "INSERT INTO ml_models (path, params, metrics, created_at) "
                    "VALUES (:p, :pa, :m, :c) RETURNING id"
                ),
                {
                    "p": path,
                    "pa": json.dumps(params),
                    "m": json.dumps(metrics),
                    "c": datetime.utcnow(),
                },
            )
            return res.scalar()
    except Exception as e:
        print(f"[Postgres] Failed to save metadata: {e}")
        return None


# ============================================================
# Step 6: Full training pipeline
# ============================================================
def run_training_pipeline(model_type="rf"):
    df = fetch_analytics_data()
    X, y = preprocess(df)
    features = list(X.columns)

    # Ensure experiment ID is set correctly each time
    with mlflow.start_run(experiment_id=exp_id):
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("n_features", len(features))

        model, metrics, X_test, y_test, preds = train_and_evaluate(X, y, model_type)

        # Log metrics
        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        # Log model safely (disable registered_model_name to avoid 404)
        mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=None)

        # Save locally
        saved_path = save_model_local(model, features)
        mlflow.log_artifact(saved_path, artifact_path="saved_models")

        # Save predictions
        preds_path = os.path.join(MODEL_SAVE_DIR, f"preds_{int(time.time())}.csv")
        pd.DataFrame({"y_true": y_test, "y_pred": preds}).to_csv(preds_path, index=False)
        mlflow.log_artifact(preds_path, artifact_path="predictions")

        # Record metadata (optional)
        params = {"model_type": model_type, "features": features}
        # mongo_id = record_metadata_mongo(saved_path, metrics, params)
        # pg_id = record_metadata_postgres(saved_path, metrics, params)

        summary = {
            "saved_path": saved_path,
            "mlflow_run_id": mlflow.active_run().info.run_id,
            "metrics": metrics,
            "mongo_id": None,
            "postgres_id": None,
        }

        print("Training Summary:", json.dumps(summary, indent=2))
        return summary


# ============================================================
# Step 7: CLI entry point
# ============================================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-type", choices=["rf", "lr"], default="rf")
    args = parser.parse_args()
    result = run_training_pipeline(args.model_type)
    print("Pipeline completed successfully.")

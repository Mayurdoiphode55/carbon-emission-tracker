import pandas as pd
import numpy as np
import xgboost as xgb
import mlflow
import mlflow.xgboost
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Configuration
MODEL_PATH = "model.pkl"
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")

def generate_synthetic_training_data(n_samples=10000):
    """Generate synthetic data for initial training since we don't have historical data yet."""
    np.random.seed(42)
    
    # Feature generation
    vehicle_count = np.random.randint(50, 500, n_samples)
    avg_speed = np.random.randint(10, 80, n_samples)
    humidity = np.random.randint(30, 90, n_samples)
    temperature = np.random.randint(20, 40, n_samples)
    
    # Simple encoded features (0: Clear, 1: Rainy, etc.)
    weather_encoded = np.random.randint(0, 4, n_samples) 
    vehicle_type_encoded = np.random.randint(0, 4, n_samples) # 0: Car, 1: Bike, etc.
    
    # Target: CO2 Emission (Just a rough formula for correlation)
    # CO2 increases with vehicle count, decreases slightly with optimal speed, increases with bad weather/temp
    co2 = (vehicle_count * 0.5) + (1000 / (avg_speed + 1)) + (weather_encoded * 10) + np.random.normal(0, 5, n_samples)
    
    df = pd.DataFrame({
        "vehicle_count": vehicle_count,
        "avg_speed": avg_speed,
        "humidity": humidity,
        "temperature": temperature,
        "weather_encoded": weather_encoded,
        "vehicle_type_encoded": vehicle_type_encoded,
        "co2_emissions": co2
    })
    
    return df

def train():
    print("Generating synthetic training data...")
    df = generate_synthetic_training_data()
    
    X = df.drop("co2_emissions", axis=1)
    y = df["co2_emissions"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("carbon_emission_prediction")
    
    with mlflow.start_run():
        print("Training XGBoost Regressor...")
        model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
        model.fit(X_train, y_train)
        
        predictions = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        
        print(f"Model trained. RMSE: {rmse}")
        
        # Log metrics and model
        mlflow.log_metric("rmse", rmse)
        mlflow.xgboost.log_model(model, "model")
        
        # Save locally for easy loading by inference service
        joblib.dump(model, MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()

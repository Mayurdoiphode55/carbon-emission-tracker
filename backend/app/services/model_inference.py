import joblib
import pandas as pd
import os

# Path to model. In Docker, we might mount this or bake it in.
# For now, we look in a likely shared location or local.
MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")

class CarbonModel:
    def __init__(self, model_path=MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.load_model()
        
    def load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print(f"Model loaded from {self.model_path}")
            else:
                print(f"Model not found at {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")

    def predict(self, features):
        if not self.model:
            # Fallback mock if model missing (to prevent API crash during dev)
            # CO2 rough calc: vehicle_count * 0.5 + 100
            return (features.get("vehicle_count", 0) * 0.5) + 100
            
        weather_map = {"Clear": 0, "Rainy": 1, "Cloudy": 2, "Foggy": 3}
        vtype_map = {"Car": 0, "Bike": 1, "Bus": 2, "Truck": 3}
        
        df = pd.DataFrame([{
            "vehicle_count": features.get("vehicle_count"),
            "avg_speed": features.get("avg_speed"),
            "humidity": features.get("humidity"),
            "temperature": features.get("temperature"),
            "weather_encoded": weather_map.get(features.get("weather"), 0),
            "vehicle_type_encoded": vtype_map.get(features.get("vehicle_type"), 0)
        }])
        
        prediction = self.model.predict(df)
        return float(prediction[0])

# Global instance
model_service = CarbonModel()

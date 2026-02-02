import joblib
import pandas as pd
import os

class CarbonModel:
    def __init__(self, model_path="model.pkl"):
        self.model_path = model_path
        self.model = None
        self.load_model()
        
    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print("Model loaded successfully.")
        else:
            print(f"Model file not found at {self.model_path}. Please train first.")
            self.model = None

    def predict(self, features):
        """
        Args:
            features (dict): Dictionary containing:
                - vehicle_count
                - avg_speed
                - humidity
                - temperature
                - weather (string to be encoded)
                - vehicle_type (string to be encoded)
        """
        if not self.model:
            raise Exception("Model not loaded")
            
        # Simple encoding mapping matching training generation
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

if __name__ == "__main__":
    # Test run
    model = CarbonModel()
    if model.model:
        pred = model.predict({
            "vehicle_count": 200,
            "avg_speed": 40,
            "humidity": 60,
            "temperature": 30,
            "weather": "Clear",
            "vehicle_type": "Car"
        })
        print(f"Test Prediction: {pred}")

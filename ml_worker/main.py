from fastapi import FastAPI

app = FastAPI(title="ML Worker Service")

@app.get("/")
def root():
    return {"message": "ML Worker service is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Example placeholder routes (optional for Phase 5)
@app.post("/train")
def train_model():
    return {"message": "Model training initiated"}

@app.post("/predict")
def predict():
    return {"message": "Prediction endpoint active"}

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.services.websocket_manager import manager
from app.services.kafka_consumer import start_consumer
from app.routers import user_router, ml_routes

app = FastAPI(title="Carbon Emission Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Start Kafka Consumer
    await start_consumer()

@app.get("/")
def root():
    return {"message": "Carbon Emission Tracker Backend Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, maybe receive commands from client
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Routers
app.include_router(user_router.router)
app.include_router(ml_routes.router)

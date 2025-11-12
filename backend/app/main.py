from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random

from app import db, crud
from app.schemas import AggregationResponse
from app.routers import user_router

app = FastAPI(title="Carbon Emission Tracker API")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- root route ----
@app.get("/")
def root():
    return {"message": "Carbon Emission Tracker Backend is running"}

# ---- lifecycle events ----
@app.on_event("startup")
async def startup():
    # Database connect disabled for local frontend testing.
    # Uncomment the next line when your database is reachable.
    # await db.database.connect()
    return

@app.on_event("shutdown")
async def shutdown():
    # await db.database.disconnect()
    return


@app.get("/health")
def health():
    return {"status": "ok"}

# ---- include existing router ----
app.include_router(user_router.router)

# ---- new analytics endpoints (Phase 4A) ----
@app.get("/analytics/avg_speed_by_road", response_model=AggregationResponse)
async def avg_speed_by_road():
    try:
        data = await crud.avg_speed_by_road()
        return {"query": "avg_speed_by_road", "results": data}
    except Exception:
        raise HTTPException(status_code=503, detail="Database error")

@app.get("/analytics/vehicle_count_by_type", response_model=AggregationResponse)
async def vehicle_count_by_type():
    data = await crud.total_vehicle_count_by_type()
    return {"query": "vehicle_count_by_type", "results": data}

@app.get("/analytics/occupancy_trend", response_model=AggregationResponse)
async def occupancy_trend(
    hours: int = Query(24, ge=1, le=168),
    interval_minutes: int = Query(60, ge=1, le=1440)
):
    data = await crud.occupancy_trends(hours=hours, interval_minutes=interval_minutes)
    return {"query": "occupancy_trend", "results": data}

# ---- mock analytics data endpoint (needed for ML worker training) ----
@app.get("/analytics/data")
async def analytics_data():
    """
    Temporary endpoint providing mock analytics data
    for the ML worker training pipeline.
    Replace with real DB query when available.
    """
    data = []
    for i in range(100):
        data.append({
            "id": i + 1,
            "temperature": round(random.uniform(20, 35), 2),
            "distance": round(random.uniform(1, 10), 2),
            "fuel_used": round(random.uniform(3, 12), 2),
            "emissions": round(random.uniform(100, 250), 2)
        })
    return JSONResponse(content=data)

# ---- ML retraining and prediction routes (Phase 5) ----
from app.routers import ml_routes
app.include_router(ml_routes.router)

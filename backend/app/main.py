from fastapi import FastAPI, Query, HTTPException
from app import db, crud
from app.schemas import AggregationResponse
from app.routers import user_router

app = FastAPI(title="Carbon Emission Tracker API")

# ---- lifecycle events ----
@app.on_event("startup")
async def startup():
    await db.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()

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
async def occupancy_trend(hours: int = Query(24, ge=1, le=168), interval_minutes: int = Query(60, ge=1, le=1440)):
    data = await crud.occupancy_trends(hours=hours, interval_minutes=interval_minutes)
    return {"query": "occupancy_trend", "results": data}

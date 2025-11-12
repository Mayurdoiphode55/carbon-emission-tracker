from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class AvgSpeedByRoad(BaseModel):
    road_type: str
    avg_speed_kmph: float

class VehicleCountByType(BaseModel):
    vehicle_type: str
    count: int

class OccupancyTrendPoint(BaseModel):
    timestamp: datetime
    avg_occupancy: float

class AggregationResponse(BaseModel):
    query: str
    results: List[Dict]

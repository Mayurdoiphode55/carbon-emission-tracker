from pydantic import BaseModel, Field, conint, confloat
from typing import Optional
from datetime import datetime


class Location(BaseModel):
    lat: confloat(ge=-90, le=90)
    lon: confloat(ge=-180, le=180)


class Weather(BaseModel):
    source: Optional[str] = None
    temperature: Optional[confloat(ge=-100, le=100)] = None
    humidity: Optional[confloat(ge=0, le=100)] = None


class TrafficEvent(BaseModel):
    event_id: str
    timestamp: datetime
    vehicle_count: conint(ge=0)
    avg_speed_kph: Optional[confloat(ge=0)] = None
    avg_speed_kmph: Optional[confloat(ge=0)] = None  # handle both spellings
    occupancy: Optional[confloat(ge=0, le=1)] = None
    road_id: Optional[str] = None
    road_type: Optional[str] = None
    location: Optional[Location] = None
    weather: Optional[Weather] = None

    class Config:
        extra = "ignore"  # ignore any unlisted extra keys

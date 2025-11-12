import asyncio
import json
import random
from datetime import datetime, timezone
from faker import Faker
import aiohttp
from kafka import KafkaProducer

fake = Faker()

# Kafka configuration
KAFKA_BROKERS = ["localhost:9092"]
TOPIC = "traffic.events"

# Open-Meteo API (no key needed)
OPENMETEO_URL = "https://api.open-meteo.com/v1/forecast"

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=5,
    retries=5
)

async def fetch_openmeteo(session, lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m",
        "timezone": "UTC"
    }
    async with session.get(OPENMETEO_URL, params=params, timeout=10) as resp:
        if resp.status == 200:
            data = await resp.json()
            # Extract current hour data if available
            hourly = data.get("hourly", {})
            return {
                "source": "open-meteo",
                "temperature": hourly.get("temperature_2m", [None])[0],
                "humidity": hourly.get("relativehumidity_2m", [None])[0]
            }
        return {"source": "open-meteo", "error": f"HTTP_{resp.status}"}

def generate_traffic_event():
    lat, lon = float(fake.latitude()), float(fake.longitude())
    return {
        "event_id": fake.uuid4(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": {"lat": lat, "lon": lon},
        "road_type": random.choice(["highway", "arterial", "local"]),
        "vehicle_count": random.randint(0, 200),
        "avg_speed_kmph": round(random.uniform(10, 120), 2),
        "occupancy": round(random.uniform(0.0, 1.0), 3)
    }

async def produce_events(rate_per_second=2):
    async with aiohttp.ClientSession() as session:
        while True:
            event = generate_traffic_event()
            weather = await fetch_openmeteo(session, event["location"]["lat"], event["location"]["lon"])
            event["weather"] = weather

            producer.send(TOPIC, value=event)
            producer.flush()
            print(f"Published event: {event['event_id']} at {event['timestamp']}")
            await asyncio.sleep(1.0 / rate_per_second)

if __name__ == "__main__":
    try:
        asyncio.run(produce_events(rate_per_second=2))
    except KeyboardInterrupt:
        print("Stopped by user.")
        producer.close()

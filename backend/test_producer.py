from confluent_kafka import Producer
import json
from datetime import datetime

p = Producer({'bootstrap.servers': 'localhost:9092'})
payload = {
  "event_id": "evt-123",
  "timestamp": datetime.utcnow().isoformat(),
  "vehicle_count": 12,
  "avg_speed_kph": 42.5,
  "road_id": "R-42",
  "location": {"lat": 18.5204, "lon":73.8567}
}
p.produce("traffic.events", json.dumps(payload).encode("utf-8"))
p.flush()

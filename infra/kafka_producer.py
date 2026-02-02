import json
import time
import random
import os
from kafka import KafkaProducer
from datetime import datetime

# Configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC_NAME = "traffic_data"

def create_producer():
    attempt = 0
    while attempt < 10:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print(f"Connected to Kafka at {KAFKA_BROKER}")
            return producer
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5s...")
            time.sleep(5)
            attempt += 1
    raise Exception("Could not connect to Kafka")

def generate_traffic_data():
    cities = ["Mumbai", "Pune", "Delhi", "Bangalore"]
    vehicle_types = ["Car", "Bike", "Bus", "Truck"]
    weather_conditions = ["Clear", "Rainy", "Cloudy", "Foggy"]

    data = {
        "timestamp": datetime.now().isoformat(),
        "location": random.choice(cities),
        "vehicle_count": random.randint(50, 500),
        "avg_speed": random.randint(10, 80),
        "vehicle_type": random.choice(vehicle_types),
        "weather": random.choice(weather_conditions),
        "humidity": random.randint(30, 90),
        "temperature": random.randint(20, 40)
    }
    return data

def main():
    producer = create_producer()
    print(f"Starting traffic simulation. Sending to topic '{TOPIC_NAME}'...")
    
    try:
        while True:
            traffic_event = generate_traffic_data()
            producer.send(TOPIC_NAME, traffic_event)
            print(f"Sent: {traffic_event}")
            time.sleep(2)  # Simulate real-time stream delay
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        producer.close()

if __name__ == "__main__":
    main()

import os
import json
import logging
from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
from pydantic import ValidationError
from dotenv import load_dotenv
from models import TrafficEvent
from datetime import datetime

load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_GROUP = os.getenv("KAFKA_GROUP", "traffic-consumer-group")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "traffic.events")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "carbon_tracker")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "traffic_events")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Configure consumer
conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP,
    'group.id': KAFKA_GROUP,
    'auto.offset.reset': 'earliest',   # or 'latest'
    'enable.auto.commit': False        # commit manually after DB write
}
consumer = Consumer(conf)
consumer.subscribe([KAFKA_TOPIC])

# Mongo client
mongo = MongoClient(MONGO_URI)
collection = mongo[MONGO_DB][MONGO_COLLECTION]

def process_message(msg):
    try:
        raw = msg.value().decode("utf-8")
        payload = json.loads(raw)
    except Exception as e:
        logging.error("Invalid JSON payload: %s", e)
        return False

    try:
        event = TrafficEvent.model_validate(payload)
    except ValidationError as ve:
        logging.error("ValidationError: %s", ve)
        return False

    doc = event.model_dump()
    # Optionally add ingestion metadata
    doc["_ingested_at"] = datetime.utcnow()

    try:
        res = collection.insert_one(doc)
        logging.info("Inserted _id=%s for event_id=%s", res.inserted_id, doc.get("event_id"))
        return True
    except Exception as e:
        logging.exception("MongoDB insert failed: %s", e)
        return False

def main():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                logging.error("Kafka error: %s", msg.error())
                continue

            success = process_message(msg)
            if success:
                # commit offset for this message
                consumer.commit(message=msg)
            else:
                # decide: log/route to DLQ. Here we simply continue.
                logging.warning("Message processing failed; offset not committed.")
    except KeyboardInterrupt:
        logging.info("Shutting down consumer.")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()

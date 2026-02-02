import asyncio
import json
import os
import threading
from kafka import KafkaConsumer
from app.services.websocket_manager import manager
from app import crud

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:29092")
TOPIC = "emission_data"

def consume_loop(loop):
    """
    Synchronous loop to consume messages from Kafka.
    """
    consumer = None
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            # We use a group id to ensure we join the group
            group_id="backend_consumer_group",
            auto_offset_reset='latest'
        )
        print(f"Kafka Consumer connected to {TOPIC}")
    except Exception as e:
        print(f"Failed to connect consumer (will retry setup): {e}")
        return

    for message in consumer:
        data = message.value
        print(f"Received emission data: {data.get('predicted_co2', 'N/A')}", flush=True)
        # 1. Broadcast to WebSockets
        asyncio.run_coroutine_threadsafe(manager.broadcast(data), loop)
        
        # 2. Persist to DB
        asyncio.run_coroutine_threadsafe(crud.create_emission_record(data), loop)

async def start_consumer():
    """
    Starts the consumer loop in a separate thread.
    """
    print("Initializing Kafka Consumer Service...")
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=consume_loop, args=(loop,), daemon=True)
    t.start()
    print("Kafka Consumer thread started.")

import json
import os
import sys
import time
from kafka import KafkaConsumer, KafkaProducer
from predict import CarbonModel

# Configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:29092")
INPUT_TOPIC = "traffic_data"
OUTPUT_TOPIC = "emission_data"

def log(msg):
    print(msg, flush=True)

def main():
    log("Starting ML Streaming Service...")
    
    # Initialize Model - train if not exists
    model = CarbonModel()
    if not model.model:
        log("Model not found! Training now...")
        import train
        train.train()
        model.load_model()
        log("Model trained and loaded!")

    
    # Initialize Kafka
    consumer = None
    producer = None
    
    # Retry connection logic
    for i in range(10):
        try:
            consumer = KafkaConsumer(
                INPUT_TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                auto_offset_reset='latest'
            )
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            log("Connected to Kafka.")
            break
        except Exception as e:
            log(f"Waiting for Kafka... ({e})")
            time.sleep(5)
            
    if not consumer or not producer:
        log("Failed to connect to Kafka. Exiting.")
        return

    log(f"Listening on {INPUT_TOPIC}...")
    
    for message in consumer:
        data = message.value
        # Expected data: timestamp, vehicle_count, avg_speed, weather, ...
        
        try:
            # Predict
            # If model is missing, we can't predict. 
            if model.model:
                predicted_co2 = model.predict(data)
                
                result = {
                    "original_data": data,
                    "predicted_co2": predicted_co2,
                    "model_version": "v1",
                    "processed_at": time.time()
                }
                
                # Send to output topic
                producer.send(OUTPUT_TOPIC, result)
                log(f"Processed: {data['location']} -> {predicted_co2:.2f} g/km")
            else:
                log("Skipping prediction (model not loaded)")
                
        except Exception as e:
            log(f"Error processing message: {e}")

if __name__ == "__main__":
    main()

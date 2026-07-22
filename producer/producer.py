import json
import random
import time
from datetime import datetime, timezone

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


def create_producer():
    while True:
        try:
            print("Connecting to Kafka...")
            producer = KafkaProducer(
                bootstrap_servers="kafka:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            print("Connected to Kafka.")
            return producer

        except NoBrokersAvailable:
            print("Kafka not ready, retrying in 5 seconds...")
            time.sleep(5)


producer = create_producer()


while True:
    now = datetime.now(timezone.utc)

    event = {
        "trip_id": str(random.randint(100000, 999999)),
        "pickup_datetime": now.isoformat(),
        "passenger_count": random.randint(1, 4),
        "trip_distance": round(random.uniform(1, 20), 2),
        "pickup_location_id": random.randint(1, 263),
        "dropoff_location_id": random.randint(1, 263),
    }

    producer.send("taxi-trips", event)
    producer.flush()

    print("Sent:", event)

    time.sleep(2)

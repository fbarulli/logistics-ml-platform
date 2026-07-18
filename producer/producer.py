from logistics_ml.schemas.taxi import TaxiTripEvent
import json
import time
import random
from datetime import datetime, timezone

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


def create_producer():
    while True:
        try:
            print("connecting to kafka...")
            producer = KafkaProducer(
                bootstrap_servers="kafka:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            print("connected to kafka")
            return producer

        except NoBrokersAvailable:
            print("kafka not ready, retrying...")
            time.sleep(5)


producer = create_producer()


while True:
    event = TaxiTripEvent(
        trip_id=str(random.randint(100000, 999999)),
        pickup_zone=random.randint(1, 50),
        dropoff_zone=random.randint(1, 50),
        distance_km=round(random.uniform(1, 20), 2),
        passengers=random.randint(1, 4),
        timestamp=datetime.now(timezone.utc),
    )

    producer.send(
        "taxi-trips",
        event.model_dump(mode="json"),
    )
    producer.flush()

    print("sent:", event)

    time.sleep(2)

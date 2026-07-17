import json
import time

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable


def create_consumer():
    while True:
        try:
            print("connecting to kafka...")

            consumer = KafkaConsumer(
                "taxi-trips",
                bootstrap_servers="kafka:9092",
                auto_offset_reset="earliest",
                group_id="taxi-debug",
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            )

            print("connected to kafka")
            return consumer

        except NoBrokersAvailable:
            print("kafka not ready, retrying...")
            time.sleep(5)


consumer = create_consumer()

print("waiting for events...")

for message in consumer:
    print("received:", message.value)

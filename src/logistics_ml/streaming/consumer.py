import json
import logging
import time
import psycopg
import requests
from kafka import KafkaConsumer
from kafka.errors import KafkaTimeoutError
from logistics_ml.features.schema import STREAM_FEATURE_TYPES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


def create_consumer() -> KafkaConsumer:
    while True:
        try:
            logger.info("Connecting to Kafka...")
            consumer = KafkaConsumer(
                "taxi-features",
                bootstrap_servers="kafka:9092",
                auto_offset_reset="earliest",
                group_id="taxi-debug",
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            )
            logger.info("Connected to Kafka.")
            return consumer

        except KafkaTimeoutError:
            logger.warning("Kafka not ready. Retrying in 5 seconds...")
            time.sleep(5)


def create_connection():
    while True:
        try:
            logger.info("Connecting to PostgreSQL...")
            conn = psycopg.connect(
                host="postgres",
                dbname="logistics",
                user="logistics",
                password="logistics",
            )
            conn.autocommit = True
            logger.info("Connected to PostgreSQL.")
            return conn

        except Exception:
            logger.warning("PostgreSQL not ready. Retrying in 5 seconds...")
            time.sleep(5)


consumer = create_consumer()
conn = create_connection()

logger.info("Waiting for feature events...")


for message in consumer:
    try:
        event = message.value

        payload = {
            name: event[name]
            for name in STREAM_FEATURE_TYPES
        }

        while True:
            try:
                response = requests.post(
                    "http://api:8000/predict",
                    json=payload,
                    timeout=10,
                )
                response.raise_for_status()
                break

            except requests.exceptions.RequestException:
                logger.warning("API unavailable. Retrying in 5 seconds...")
                time.sleep(5)

        prediction = response.json()["prediction"]

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO taxi_predictions (
                    trip_id,
                    prediction
                )
                VALUES (%s, %s)
                """,
                (
                    event["trip_id"],
                    prediction,
                ),
            )

        logger.info(
            "Trip %s predicted %.2f minutes",
            event["trip_id"],
            prediction,
        )

    except Exception:
        logger.exception("Failed processing event")

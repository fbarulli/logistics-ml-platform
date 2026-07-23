from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataConfig:

    raw_data_dir: Path = Path("data/raw")

    taxi_lookup: Path = raw_data_dir / "taxi_zone_lookup.csv"

    training_table: str = "training_data"

    target: str = "trip_duration_minutes"

    validation_cutoff: str = "2024-03-01"

    taxi_urls: tuple[str, ...] = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet",
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet",
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet",
    )


data = DataConfig()

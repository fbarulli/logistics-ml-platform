# src/logistics_ml/config/features.py
from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureConfig:

    features = [

        "pickup_hour",
        "pickup_day_of_week",
        "pickup_month",

        "passenger_count",

        "trip_distance",

        "pickup_location_id",
        "dropoff_location_id",

        "route_avg_duration",
        "route_frequency",

        "is_weekend",
        "rush_hour",
        "is_night",
        "is_large_group",

        "same_borough",

    ]


features = FeatureConfig()

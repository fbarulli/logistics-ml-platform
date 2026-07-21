from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split

from logistics_ml.config import data as data_config
from logistics_ml.config import training as training_config

from .basic import add_basic_features
from .boroughs import add_borough_features, load_zones
from .encodings import (
    apply_target_encoding,
    make_target_encoding,
)
from .frequency import (
    apply_frequency_encoding,
    make_frequency_encoding,
)


FEATURE_COLUMNS = [
    "pickup_hour",
    "pickup_day_of_week",
    "pickup_month",
    "passenger_count",
    "trip_distance",
    "pickup_location_id",
    "dropoff_location_id",
    "is_weekend",
    "rush_hour",
    "is_night",
    "log_distance",
    "same_borough",
    "route_avg_duration",
    "route_frequency",
]


TARGET = "trip_duration_minutes"


def prepare_dataset(df: pd.DataFrame):

    zones = load_zones(data_config.taxi_lookup)

    # ----------------------------
    # Deterministic features
    # ----------------------------

    df = add_basic_features(df)
    df = add_borough_features(df, zones)

    # ----------------------------
    # Time split
    # ----------------------------

    cutoff = pd.Timestamp(training_config.train_test_cutoff)

    train_df = df[df["pickup_datetime"] < cutoff].copy()
    test_df = df[df["pickup_datetime"] >= cutoff].copy()

    # ----------------------------
    # Historical route average
    # ----------------------------

    global_mean = train_df[TARGET].mean()

    route_stats, _ = make_target_encoding(
        train_df,
        ["pickup_location_id", "dropoff_location_id"],
        TARGET,
        "route_avg_duration",
    )

    train_df = apply_target_encoding(
        train_df,
        route_stats,
        ["pickup_location_id", "dropoff_location_id"],
        "route_avg_duration",
        global_mean,
    )

    test_df = apply_target_encoding(
        test_df,
        route_stats,
        ["pickup_location_id", "dropoff_location_id"],
        "route_avg_duration",
        global_mean,
    )

    # ----------------------------
    # Route frequency
    # ----------------------------

    route_freq = make_frequency_encoding(
        train_df,
        ["pickup_location_id", "dropoff_location_id"],
        "route_frequency",
    )

    train_df = apply_frequency_encoding(
        train_df,
        route_freq,
        ["pickup_location_id", "dropoff_location_id"],
        "route_frequency",
    )

    test_df = apply_frequency_encoding(
        test_df,
        route_freq,
        ["pickup_location_id", "dropoff_location_id"],
        "route_frequency",
    )

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df[TARGET]

    X_test = test_df[FEATURE_COLUMNS]
    y_test = test_df[TARGET]

    return X_train, X_test, y_train, y_test

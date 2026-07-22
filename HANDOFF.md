# Logistics ML Platform — FeaturePipeline Handoff

## Summary

This pass introduced `FeaturePipeline` as a reusable, statistically-fitted
object, replacing the old function-based `prepare_dataset()` flow. It also
fixed two hidden production bugs along the way:

1. **Serving mismatch** — the registered model previously stored only the raw
   `XGBoostModel`, fit on 14 engineered features, while `service/app.py` sent
   7 unrelated columns. This would have failed or silently mispredicted.
2. **Stale training image** — `make train` ran against a `kind`-cached Docker
   image that was never reloaded into the cluster, so code changes silently
   had no effect until `kind load docker-image` was added.

## Flow (text form)

```
TRAINING (k8s Job: training)
  Postgres training_data table
    -> load_training_data()
    -> prepare_dataset(df)
         -> time-based split into train_df / test_df
         -> FeaturePipeline().fit(train_df)
              -> add_basic_features        (time + trip features)
              -> add_borough_features       (zone lookup merge)
              -> make_target_encoding       (route_avg_duration, smoothed)
              -> make_frequency_encoding    (route_frequency)
              -> stores fitted state: zones, route_stats,
                 route_frequency, global_mean
         -> FeaturePipeline.transform(train_df) / transform(test_df)
              -> re-applies basic + borough features
              -> applies target + frequency encoding using fitted state
              -> row-count guard: raises if a merge changed row count
         -> returns X_train, X_test, y_train, y_test, pipeline
    -> get_model("xgb") -> XGBoostModel.fit(X_train, y_train)
    -> evaluate(model, X_test, y_test) -> MAE / RMSE / R2
    -> TaxiDurationPyfuncModel(feature_pipeline, model)
    -> mlflow.pyfunc.log_model(python_model=wrapped, input_example=...)
         -> signature inferred and stored
    -> registered in MLflow Model Registry as taxi-duration-model vN
    -> set_registered_model_alias(alias="champion")

SERVING (k8s Deployment: service)
  POST /predict  (TaxiTrip, built dynamically from RAW_FEATURE_TYPES)
    -> pd.DataFrame from raw payload
    -> mlflow.pyfunc.load_model("models:/taxi-duration-model@champion")
    -> TaxiDurationPyfuncModel.predict(raw_df)
         -> self.feature_pipeline.transform(raw_df)  (same class as training)
         -> self.model.predict(engineered_df)
    -> JSON response: prediction, latency_ms

SINGLE SOURCE OF TRUTH
  features/schema.py defines:
    RAW_FEATURES, RAW_FEATURE_TYPES, ENGINEERED_FEATURES, TARGET, ROUTE_KEYS
  Used by: prepare_dataset, FeaturePipeline, service/app.py's TaxiTrip model
```

## Key files and their roles

| File | Role |
|---|---|
| `features/schema.py` | Single source of truth for raw and engineered feature names/types. Everything else derives from this. |
| `features/feature_pipeline.py` | `FeaturePipeline` — `fit()` learns zone lookups, target encoding, frequency encoding from train data; `transform()` applies them + raises if a merge silently changes row count. |
| `features/pipeline.py` | `prepare_dataset()` — does the time-based train/test split, then delegates all feature engineering to `FeaturePipeline`. Returns `X_train, X_test, y_train, y_test, pipeline`. |
| `models/pyfunc_wrapper.py` | `TaxiDurationPyfuncModel` — bundles a fitted `FeaturePipeline` + trained model into one MLflow pyfunc artifact, so raw input goes in and a prediction comes out. |
| `training.py` | Orchestrates: load data -> `prepare_dataset` -> train -> evaluate -> wrap -> register -> set `champion` alias. |
| `mlflow_utils.py` | `log_model()` now logs via `mlflow.pyfunc.log_model` (was `mlflow.sklearn.log_model`), with `input_example` so MLflow can infer and store a schema signature. |
| `service/app.py` | FastAPI `/predict`. Input model (`TaxiTrip`) is now built dynamically from `RAW_FEATURE_TYPES` instead of a hardcoded 7-field list. Loads the `champion`-aliased pyfunc model and calls `.predict()` directly — no manual feature engineering here anymore. |
| `k8s/training-job.yaml` | Runs the training image as a one-off Job. Image must be rebuilt + `kind load`-ed for changes to take effect (see `Makefile`). |
| `Makefile` (`make train`) | `docker build` -> `kind load docker-image` -> delete old Job -> apply -> wait for pod ready -> tail logs. Previously missing the `kind load` step, which caused silent staleness. |

## Known follow-ups (not yet done)

- **Verify `/predict` end-to-end** against the new pyfunc artifact (version 10+) — not yet confirmed live against `service/app.py`.
- **`service` deployment model refresh strategy** — unconfirmed whether the running `service` pod auto-polls the `champion` alias or needs a restart to pick up a newly registered version. Needs a look at `k8s/service-deployment.yaml`.
- **`src/logistics_ml/serving.py`** — appears to be dead code (a second, unused `predict()` path with its own model-loading logic, inconsistent with `service/app.py`). Candidate for deletion in a cleanup pass.
- **Two orphaned/conflicting input schemas found during this work**: `schemas/taxi.py`'s `TaxiTripEvent` (pickup_zone/dropoff_zone/distance_km/passengers) doesn't match anything currently wired up. Worth confirming whether it's still needed (e.g. for a Kafka/streaming payload) or also dead.
- **Dead `config/features.py`** was removed (a stale, out-of-sync feature list superseded by `features/schema.py`); no functional replacement was needed since `schema.py` already served that purpose.

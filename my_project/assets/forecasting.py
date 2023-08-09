from dagster import (
    asset,
    AssetExecutionContext,
    AssetKey,
    DailyPartitionsDefinition,
    FreshnessPolicy,
)

import pandas as pd
import time

import random

daily_partitions = DailyPartitionsDefinition(start_date="2023-04-01")

country_population = AssetKey(["population", "country_population"])
continent_population = AssetKey(["population", "continent_population"])

@asset(
    deps=[continent_population],
    compute_kind="DuckDB",
    partitions_def=daily_partitions,
    metadata={"partition_expr": "date"},
)
def continent_feature(context) -> pd.DataFrame:
    """Feature based on continent population data"""
    partition_date_str = context.asset_partition_key_for_output()

    time.sleep(3)
    return pd.DataFrame([{"foo": "bar", "date": partition_date_str }])


@asset(
    deps=[country_population],
    compute_kind="DuckDB",
    partitions_def=daily_partitions,
    metadata={"partition_expr": "date"},
)
def country_feature(context) -> pd.DataFrame:
    """Feature based on country population data"""
    partition_date_str = context.asset_partition_key_for_output()

    time.sleep(1)
    return pd.DataFrame([{"foo": "bar", "date": partition_date_str }])

@asset(
    deps=[continent_feature, country_feature],
    compute_kind="TensorFlow",
)
def population_forecast_model() -> pd.DataFrame:
    """Trained ML model for forecasting population"""
    time.sleep(2)
    return pd.DataFrame([{"foo": random.random() * 100}])


@asset(
    deps=[population_forecast_model],
    freshness_policy=FreshnessPolicy(maximum_lag_minutes=24 * 60),
    compute_kind="Python",
)
def forecasted_population(context: AssetExecutionContext) -> pd.DataFrame:
    """Table containing forecasted population data"""

    context.add_output_metadata({
        "param_value": int((random.random() / 2 + 0.5)),
        "accuracy": (65 - (10 * random.random()) + 1 / 6) / 100.0,
    })
    return pd.DataFrame([{"foo": "bar"}])

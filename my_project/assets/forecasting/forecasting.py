from typing import Any, Tuple

import pandas as pd
from dagster import AssetIn, asset, DailyPartitionsDefinition, Output, FreshnessPolicy
import time

import random

daily_partitions = DailyPartitionsDefinition(start_date="2023-04-01")


@asset(
    ins={"continent_population": AssetIn(["population", "continent_population"])},
    compute_kind="DuckDB",
    partitions_def=daily_partitions,
    metadata={"partition_expr": "date"},
)
def continent_feature(context, continent_population: pd.DataFrame) -> pd.DataFrame:
    """Feature based on continent population data"""
    partition_date_str = context.asset_partition_key_for_output()

    time.sleep(3)
    return pd.DataFrame([{"foo": "bar", "date": partition_date_str }])


@asset(
    ins={"country_population": AssetIn(["population", "country_population"])},
    compute_kind="DuckDB",
    partitions_def=daily_partitions,
    metadata={"partition_expr": "date"},
)
def country_feature(context, country_population: pd.DataFrame) -> pd.DataFrame:
    """Feature based on country population data"""
    partition_date_str = context.asset_partition_key_for_output()

    time.sleep(1)
    return pd.DataFrame([{"foo": "bar", "date": partition_date_str }])

@asset(
    compute_kind="ML Tool",
)
def population_forecast_model(
    continent_feature: pd.DataFrame, country_feature: pd.DataFrame
) -> pd.DataFrame:
    """Trained ML model for forecasting population"""
    time.sleep(5)
    return pd.DataFrame([{"foo": "bar"}])


@asset(
    freshness_policy=FreshnessPolicy(maximum_lag_minutes=24 * 60),
    compute_kind="Python"
)
def forecasted_population(
    population_forecast_model: pd.DataFrame
) -> pd.DataFrame:
    """Table containing forecasted population data"""

    yield Output(
        pd.DataFrame([{"foo": "bar"}]),
        metadata={
            "param_value": int((random.random() / 2 + 0.5)),
            "accuracy": (65 - (10 * random.random()) + 1 / 6) / 100.0,
        },
    )

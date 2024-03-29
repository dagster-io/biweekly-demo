from typing import Any, Tuple

import pandas as pd
from dagster import AssetIn, asset, DailyPartitionsDefinition
import time

daily_partitions = DailyPartitionsDefinition(start_date="2022-06-01")


@asset(
    ins={"continent_population": AssetIn(["ben", "continent_population"])},
)
def continent_feature(continent_population: pd.DataFrame) -> pd.DataFrame:
    """Feature based on continent population data"""
    time.sleep(3)
    return pd.DataFrame([{"foo": "bar"}])


@asset(
    ins={"country_population": AssetIn(["ben", "country_population"])},
)
def country_feature(country_population: pd.DataFrame) -> pd.DataFrame:
    """Feature based on country population data"""
    time.sleep(1)
    return pd.DataFrame([{"foo": "bar"}])


@asset()
def population_forecast_model(
    continent_feature: pd.DataFrame, country_feature: pd.DataFrame
) -> pd.DataFrame:
    """Trained ML model for forecasting population"""
    time.sleep(5)
    return pd.DataFrame([{"foo": "bar"}])


@asset()
def forecasted_population(
    context,
    population_forecast_model: pd.DataFrame,  # : Tuple[float, float],
) -> pd.DataFrame:
    """Table containing forecasted population data"""
    import random
    from dagster import Output

    yield Output(
        pd.DataFrame([{"foo": "bar"}]),
        metadata={
            "param_value": int((random.random() / 2 + 0.5)),
            "accuracy": (65 - (10 * random.random()) + 1 / 6) / 100.0,
        },
    )

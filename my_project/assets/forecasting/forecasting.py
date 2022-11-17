from typing import Any, Tuple

import pandas as pd
from dagster import AssetIn, asset, DailyPartitionsDefinition
import time

daily_partitions = DailyPartitionsDefinition(start_date="2022-06-01")


@asset(
    compute_kind="feature_tool",
    ins={"continent_population": AssetIn(["raw", "continent_population"])},
)
def continent_feature(continent_population):
    """Feature based on continent population data"""
    time.sleep(3)


@asset(
    compute_kind="feature_tool",
    ins={"country_population": AssetIn(["raw", "country_population"])},
)
def country_feature(country_population):
    """Feature based on country population data"""
    time.sleep(1)


@asset(compute_kind="ml_tool")
def population_forecast_model(continent_feature, country_feature) -> Any:
    """Trained ML model for forecasting population"""
    time.sleep(5)


@asset(compute_kind="ml_tool")
def forecasted_population(
    context,
    population_forecast_model,  # : Tuple[float, float],
) -> pd.DataFrame:
    """Table containing forecasted population data"""
    import random
    from dagster import Output

    yield Output(
        None,
        metadata={
            "param_value": int((random.random() / 2 + 0.5)),
            "accuracy": (65 - (10 * random.random()) + 1 / 6) / 100.0,
        },
    )

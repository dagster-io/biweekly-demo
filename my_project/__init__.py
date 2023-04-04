from dagster import (
    load_assets_from_package_module,
    Definitions,
)
from my_project.assets import population, forecasting

from dagster_duckdb_pandas import duckdb_pandas_io_manager

population_assets = load_assets_from_package_module(
    population, group_name="population", key_prefix="population"
)

defs = Definitions(
    assets=population_assets,
    resources={
        "io_manager": duckdb_pandas_io_manager.configured({
            "database": "analytics"
        }),
    }
)

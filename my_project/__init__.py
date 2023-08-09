from dagster import (
    load_assets_from_modules,
    define_asset_job,
    AssetSelection,
    AutoMaterializePolicy,
    Definitions,
    EnvVar,
    ScheduleDefinition,
)

from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBResource
from dagster_duckdb_pandas import DuckDBPandasIOManager

from dagster_snowflake import SnowflakeResource
from dagster_snowflake_pandas import SnowflakePandasIOManager

import os

from my_project.assets import population_complete, forecasting, transformations

ENVIRONMENT = "local"
DBT_PROJECT_DIRECTORY = "./dbt_project"

population_assets = load_assets_from_modules(
    [population_complete],
    group_name="population",
    key_prefix="population",
    auto_materialize_policy=AutoMaterializePolicy.eager()
)

forecasting_assets = load_assets_from_modules(
    [forecasting],
    group_name="forecasting",
    auto_materialize_policy=AutoMaterializePolicy.eager()
)

transformation_assets = load_assets_from_modules(
    [transformations],
    group_name="transformations"
)

dbt = DbtCliResource(
    project_dir=DBT_PROJECT_DIRECTORY,
    profiles_dir=DBT_PROJECT_DIRECTORY
)

if ENVIRONMENT == "local":
    resources = {
        "database": DuckDBResource(database=os.getenv("DUCKDB_DATABASE_LOCATION")),
        "io_manager": DuckDBPandasIOManager(database=os.getenv("DUCKDB_DATABASE_LOCATION")),
        "dbt": dbt
    }
elif ENVIRONMENT == "production":
    snowflake_credentials = {
        "account": EnvVar("SNOWFLAKE_ACCOUNT"),
        "user": EnvVar("SNOWFLAKE_USER"),
        "password": EnvVar("SNOWFLAKE_PASSWORD"),
        "role": EnvVar("SNOWFLAKE_ROLE")
    }

    resources = {
        "database": SnowflakeResource(**snowflake_credentials),
        "io_manager": SnowflakePandasIOManager(**snowflake_credentials),
        "dbt": dbt
    }

defs = Definitions(
    assets=population_assets + forecasting_assets + transformation_assets,
    resources=resources,
    schedules=[
        ScheduleDefinition(
            job=define_asset_job(
                "update_forecast",
                selection=AssetSelection.groups("population")
            ),
            cron_schedule="@daily",
        ),
    ],
)

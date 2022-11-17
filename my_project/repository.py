import os
from dagster import (
    load_assets_from_package_module,
    repository,
    with_resources,
    AssetSelection,
    define_asset_job,
    ScheduleDefinition,
)
from dagster_dbt import load_assets_from_dbt_project, dbt_cli_resource

from dagster._utils import file_relative_path

from my_project.assets import population, forecasting

from dagster_snowflake import build_snowflake_io_manager
from dagster_snowflake_pandas import SnowflakePandasTypeHandler

snowflake_io_manager = build_snowflake_io_manager([SnowflakePandasTypeHandler()])


@repository
def my_repository():
    population_assets = load_assets_from_package_module(
        population, group_name="population", key_prefix="ben"
    )
    return [
        with_resources(
            population_assets,
            {
                "io_manager": snowflake_io_manager.configured(
                    {
                        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
                        "user": os.getenv("SNOWFLAKE_USER"),
                        "password": os.getenv("SNOWFLAKE_PASSWORD"),
                        "database": "SANDBOX",
                        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
                    }
                ),
            },
        ),
    ]

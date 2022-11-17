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

# 2. Add IO manager
from dagster_snowflake import build_snowflake_io_manager
from dagster_snowflake_pandas import SnowflakePandasTypeHandler

# DBT_DIR = "./my_project/my_dbt_project"

snowflake_io_manager = build_snowflake_io_manager([SnowflakePandasTypeHandler()])

DBT_PROJECT_DIR = file_relative_path(__file__, "./my_dbt_project")


@repository
def my_repository():
    # 1. Load pop assets
    population_assets = load_assets_from_package_module(
        population, group_name="population", key_prefix="ben"
    )
    # 3. Add DBT assets
    transformation_assets = load_assets_from_dbt_project(
        project_dir=DBT_PROJECT_DIR, profiles_dir=DBT_PROJECT_DIR, key_prefix="ben"
    )
    # 4. Add forecasting assets
    forecasting_assets = load_assets_from_package_module(
        forecasting, group_name="forecasting", key_prefix="ben"
    )
    return [
        # Pop Assets
        # population_assets
        # 2. Add snowflake IO manager resource
        # with_resources(
        #     population_assets ,
        #     {
        #         "io_manager": snowflake_io_manager.configured(
        #             {
        #                 "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        #                 "user": os.getenv("SNOWFLAKE_USER"),
        #                 "password": os.getenv("SNOWFLAKE_PASSWORD"),
        #                 "database": "SANDBOX",
        #                 "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        #             }
        #         ),
        #     },
        # )
        # 3. Add dbt assets
        with_resources(
            population_assets + transformation_assets + forecasting_assets,
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
                "dbt": dbt_cli_resource.configured(
                    {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROJECT_DIR}
                ),
            },
        ),
        ScheduleDefinition(
            job=define_asset_job(
                "update_forecast",
                selection=AssetSelection.keys(["ben", "forecasted_population"]).upstream(),
            ),
            cron_schedule="@hourly",
        ),
    ]

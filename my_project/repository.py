from dagster import (
    load_assets_from_package_module,
    repository,
    with_resources,
    AssetSelection,
    define_asset_job,
    ScheduleDefinition,
)
from dagster_dbt import load_assets_from_dbt_project, dbt_cli_resource

# from dagster_snowflake_pandas import snowflake_pandas_io_manager

from my_project.assets import population, forecasting, gdp

from .jobs import scaffold_cloud_resources

DBT_DIR = "./my_project/my_dbt_project"


@repository
def my_repo():
    return [
        ScheduleDefinition(
            job=define_asset_job(
                "update_summary", selection=AssetSelection.keys("population_summary").upstream()
            ),
            cron_schedule="@hourly",
        ),
        scaffold_cloud_resources,
        with_resources(
            definitions=load_assets_from_package_module(
                population,
                group_name="population",
                key_prefix="raw",
            )
            + load_assets_from_package_module(
                gdp,
                group_name="gdp",
                # key_prefix="raw",
            )
            + load_assets_from_dbt_project(
                project_dir=DBT_DIR,
                profiles_dir=DBT_DIR,
            )
            + load_assets_from_package_module(
                forecasting,
                group_name="forecasting",
            ),
            resource_defs={
                "dbt": dbt_cli_resource.configured(
                    {
                        "project_dir": DBT_DIR,
                        "profiles_dir": DBT_DIR,
                    }
                ),
                # "io_manager": snowflake_pandas_io_manager.configured(
                #     {
                #         "user": {"env": "SNOWFLAKE_USER"},
                #         "password": {"env": "SNOWFLAKE_PASSWORD"},
                #         "account": {"env": "SNOWFLAKE_ACCOUNT"},
                #         "database": {"env": "SNOWFLAKE_DATABASE"},
                #     }
                # ),
            },
        ),
    ]

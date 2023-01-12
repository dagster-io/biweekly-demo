import os
from dagster import (
    load_assets_from_package_module,
    AssetSelection,
    define_asset_job,
    ScheduleDefinition,
    Definitions,
)
from dagster_dbt import load_assets_from_dbt_project, dbt_cli_resource

from dagster._utils import file_relative_path

from my_project.assets import population, forecasting

defs = Definitions()

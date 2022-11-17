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


@repository
def my_repository():
    population_assets = load_assets_from_package_module(
        population, group_name="population", key_prefix="ben"
    )
    return [population_assets]

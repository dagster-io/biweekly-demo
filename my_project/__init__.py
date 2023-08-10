from dagster import (
    load_assets_from_modules,
    define_asset_job,
    AssetSelection,
    AutoMaterializePolicy,
    Definitions,
    ScheduleDefinition,
)

from my_project.assets import population_complete, forecasting, transformations

population_assets = load_assets_from_modules(
    [population_complete],
    group_name="population",
    key_prefix="population",
    auto_materialize_policy=AutoMaterializePolicy.eager()
)

forecasting_assets = load_assets_from_modules(
    [forecasting],
    group_name="forecasting"
)

transformation_assets = load_assets_from_modules(
    [transformations],
    group_name="transformations",
    auto_materialize_policy=AutoMaterializePolicy.eager()
)

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

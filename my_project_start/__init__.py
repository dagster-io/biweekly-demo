from dagster import (
    load_assets_from_modules,
    Definitions,
)
from my_project.assets import population_complete as population

assets = load_assets_from_modules([population])

defs = Definitions(
    assets=assets
)

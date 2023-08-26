from dagster import (
    load_assets_from_modules,
    Definitions,
)

from . import assets

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets
)

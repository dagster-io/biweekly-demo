from dagster import OpExecutionContext
from dagster_dbt import dbt_assets, DbtCliResource

from pathlib import Path


# DBT_PROJECT_DIRECTORY = "./dbt_project"
# dbt_parse_invocation = dbt.cli(["parse"], manifest={}).wait()
# dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("../manifest.json")

dbt_manifest_path = Path("./dbt_project/target/manifest.json")

@dbt_assets(manifest=dbt_manifest_path)
def dbt_assets(context: OpExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
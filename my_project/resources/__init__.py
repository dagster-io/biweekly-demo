from dagster import EnvVar


from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBResource
from dagster_duckdb_pandas import DuckDBPandasIOManager

from dagster_snowflake import SnowflakeResource
from dagster_snowflake_pandas import SnowflakePandasIOManager

import os

dbt_project_directory = os.getenv("DBT_PROJECT_DIRECTORY")
environment = os.getenv("ENVIRONMENT")

dbt = DbtCliResource(
    project_dir=dbt_project_directory,
    profiles_dir=dbt_project_directory
)

if environment == "local":
    resources = {
        "database": DuckDBResource(database=os.getenv("DUCKDB_DATABASE_LOCATION")),
        "io_manager": DuckDBPandasIOManager(database=os.getenv("DUCKDB_DATABASE_LOCATION")),
        "dbt": dbt
    }
elif environment == "production":
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
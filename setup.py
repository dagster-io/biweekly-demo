import setuptools

setuptools.setup(
    name="my_project",
    packages=setuptools.find_packages(exclude=["my_project_tests"]),
    install_requires=[
        "dagster_dbt",
        "dagster_duckdb_pandas",
        "dagster_duckdb",
        "dagster_snowflake_pandas",
        "dagster_snowflake",
        "dagster-cloud",
        "dagster-dbt",
        "dagster-webserver",
        "dagster",
        "dbt-duckdb",
        "dbt-snowflake",
        "duckdb",
        "lxml",
        "pandas",
        "pytest",
    ],
)

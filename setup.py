import setuptools

setuptools.setup(
    name="my_project",
    packages=setuptools.find_packages(exclude=["my_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dagster_snowflake",
        "dagster_snowflake_pandas",
        "dagster_dbt",
        "lxml",
        "dbt-duckdb",
        "dbt-snowflake",
        "pandas",
        "dagit",
        "pytest",
    ],
)

import setuptools

setuptools.setup(
    name="my_project",
    packages=setuptools.find_packages(exclude=["my_project_tests"]),
    install_requires=["dagster==0+dev", "dagit==0+dev", "pytest", "dbt-duckdb"],
)

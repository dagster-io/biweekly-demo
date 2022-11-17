import time
from dagster import job, op


@op
def create_snowflake_schema(context):
    """
    Scaffolds a temporary Snowflake schema for use in branch deployments.
    """
    time.sleep(5)


@job()
def scaffold_cloud_resources():
    create_snowflake_schema()

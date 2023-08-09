import pandas as pd
from dagster import asset, MetadataValue, AssetExecutionContext

from dagster_duckdb import DuckDBResource


@asset(
    compute_kind="Wikipedia",
    
)
def country_population(context: AssetExecutionContext) -> pd.DataFrame:
    """
    Population by country.
    """
    df = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    )[0]

    df.columns = ["country", "region", "subregion", "pop_2018", "pop_2019", "pct_change"]

    context.add_output_metadata({
        "preview": MetadataValue.md(df.head().to_markdown())
    })
    
    return df


@asset(
    compute_kind="DuckDB",
    deps=[country_population]
)
def continent_population(context: AssetExecutionContext , database: DuckDBResource) -> pd.DataFrame:
    """
    Population by continent.
    """

    # Notice how we're now querying the database instead of reading from a CSV.
    query = """
        select
            region as continent,
            count(1) as population_count
        from public.country_population
        group by region
    """

    with database.get_connection() as conn:
        df = conn.execute(query).fetch_df()


    context.add_output_metadata({
        "preview": MetadataValue.md(df.head().to_markdown())
    })

    return df
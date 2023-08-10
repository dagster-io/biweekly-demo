from dagster import asset

import pandas as pd

import duckdb

@asset
def country_population() -> None:
    df = pd.read_html("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)")[0]

    df.columns = ["country", "region", "subregion", "pop_2018", "pop_2019", "pct_change"]

    df.to_csv("data/population.csv", index=False)


@asset(
    deps=[country_population]
)
def continent_population() -> None:
    conn = duckdb.connect()

    query = """
        select
            region as continent,
            count(1) as population_count
        from 'data/country_population.csv'
        group by 1
    """

    df = conn.execute(query).fetch_df()

    df.to_csv("data/continent_population.csv", index=False)
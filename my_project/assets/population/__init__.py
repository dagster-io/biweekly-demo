import pandas as pd
from dagster import asset

@asset
def country_population():
    df = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    )[0]

    df.columns = ["country", "region", "subregion", "pop_2018", "pop_2019", "pct_change"]
    
    return df


@asset
def continent_population(country_population):
    grouped_by_continent = country_population.groupby("region").sum()

    return grouped_by_continent
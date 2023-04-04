import pandas as pd
from dagster import asset, Output, MetadataValue


@asset(
    compute_kind="Wikipedia"
)
def country_population() -> pd.DataFrame:
    """
    Population by country.
    """
    df = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    )[0]

    df.columns = ["country", "region", "subregion", "pop_2018", "pop_2019", "pct_change"]
    
    # return df

    yield Output(
        df,
        metadata={
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )


@asset(
    compute_kind="DuckDB"
)
def continent_population(country_population: pd.DataFrame) -> pd.DataFrame:
    """
    Population by continent.
    """

    grouped_by_continent = country_population.groupby("region").sum()

    # return grouped_by_continent

    yield Output(
        grouped_by_continent,
        metadata={
            "preview": MetadataValue.md(grouped_by_continent.to_markdown())
        }
    )

import pandas as pd
from dagster import asset


@asset
def country_population():  # -> pd.DataFrame:
    """Population per country"""
    return pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    )[0]


@asset
def continent_population(country_population):  #: pd.DataFrame) -> pd.DataFrame:
    """Population per continent"""
    return None  # country_population.groupby("UN continentalregion[4]").sum()

import pandas as pd
from dagster import AssetIn, asset


@asset
def country_gdp() -> pd.DataFrame:
    """Population per country"""
    gdp = pd.read_html("https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)")[2]
    print(gdp)
    return gdp


@asset(
    ins={
        "country_population": AssetIn(["raw", "country_population"]),
        "country_gdp": AssetIn(["country_gdp"]),
    }
)
def country_population_and_gdp(
    country_population: pd.DataFrame, country_gdp: pd.DataFrame
) -> pd.DataFrame:
    country_gdp.columns = country_gdp.columns.droplevel(0)
    population_gdp_table = pd.merge(
        country_population,
        country_gdp.iloc[:, :-4],
        how="inner",
        left_on="Country / Area",
        right_on="Country/Territory",
    )
    population_gdp_table["GDP Per Capita"] = (
        1000000
        * pd.to_numeric(population_gdp_table["Estimate"], errors="coerce")
        / population_gdp_table["Population(1 July 2019)"]
    )
    print(population_gdp_table)
    return population_gdp_table




import marimo

__generated_with = "0.13.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    import plotly.express as px
    import polars as pl
    return (pl,)


@app.cell
def _(pl):
    NYC=pl.read_csv("data/NYC_Collisions.csv",null_values="NA")
    return (NYC,)


@app.function
def get_time_of_day(time_str):
    hour = int(time_str.split(":")[0])
    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    elif 18 <= hour < 24:
        return "Evening"
    else:
        return "Night"


@app.cell
def _(NYC, pl):
    df = NYC.with_columns(
        pl.col("Time").map_elements(get_time_of_day, return_dtype=pl.Utf8).alias("Time of Day") # map_elements from "https://docs.pola.rs/api/python/stable/reference/series/api/polars.Series.map_elements.html"
    )
    df = df.drop_nulls(["Borough"])
    NYCT_clean = df.filter(pl.col("Time").is_not_null())
    grouped = (
        NYCT_clean.group_by(["Borough", "Time of Day"])
          .agg(pl.count().alias("Collision Count"))
          .sort(["Borough", "Time of Day"])
    )
    grouped
    return (grouped,)


@app.cell
def _(grouped):
    # Top 2 Boroughs with # of crashes and line charts
    top10=grouped.sort("Collision Count", descending=True).head(10)
                                                        
    top10
    return


if __name__ == "__main__":
    app.run()

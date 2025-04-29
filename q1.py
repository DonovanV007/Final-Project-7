

import marimo

__generated_with = "0.13.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    
    import plotly.express as px
    import polars as pl
    return pl, px


@app.cell
def _():
    return


@app.cell
def _(pl):
    
    NYC = pl.read_csv("data/NYC_Collisions.csv",null_values="NA")
    NYC
    return (NYC,)


@app.cell
def _(NYC, pl):
    NYCM = NYC.with_columns(
        pl.when(pl.col("Date").str.strptime(pl.Date, "%Y-%m-%d", strict=False).is_not_null())
        .then(pl.col("Date").str.strptime(pl.Date, "%Y-%m-%d", strict=False)) ##.str.strptime came from "https://docs.pola.rs/api/python/stable/reference/series/api/polars.Series.str.strptime.html"
        .otherwise(None)
        .alias("Date_clean")
    )

     
    NYCM_clean = NYCM.filter(pl.col("Date_clean").is_not_null())

    
    month_counts = (
        NYCM_clean.with_columns(pl.col("Date_clean").dt.strftime("%Y-%m").alias("Month"))
        # .dt.strftime came from "https://docs.pola.rs/api/python/stable/reference/series/api/polars.Series.dt.strftime.html"
        .group_by("Month")
    
        .len()
        .with_columns((pl.col("len") / NYCM_clean.height * 100).alias("Percent"))
        .sort("Month")
    )

    month_counts
    return (month_counts,)


@app.cell
def _(month_counts, px):
    months = month_counts["Month"].to_list()
    percent=month_counts["Percent"].to_list()

    
    fig = px.bar(
        x=months,
        y=percent,
        title="NYC Percentage of Accidents by Month",
        labels={"x": "Month", "y": "Percentage of Accidents"},
        category_orders={"x": [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]}
    )

    fig
    return


if __name__ == "__main__":
    app.run()

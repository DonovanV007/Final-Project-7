

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
def _(pl):
    NYC = pl.read_csv("data/NYC_Collisions.csv")

    NYC = NYC.with_columns([
        pl.col("Date").str.to_date(),
        pl.col("Time").str.strptime(pl.Time, "%H:%M:%S")  #https://docs.pola.rs/api/python/dev/reference/expressions/api/polars.Expr.str.strptime.html
    ])
    NYC = NYC.with_columns([
        pl.col("Date").dt.weekday().alias("day_of_week"),
        pl.col("Time").dt.hour().alias("hour_of_day")
    ])

    accidents = (
        NYC.group_by(["day_of_week", "hour_of_day"])
           .agg(pl.len().alias("accident_count"))
           .sort(["day_of_week", "hour_of_day"])
    )
    accidents

    return (accidents,)


@app.cell
def _(accidents, px):
    fig = px.density_heatmap(
        accidents.to_dict(as_series=False), #https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.to_dict.html
        x="hour_of_day",
        y="day_of_week",
        z="accident_count",
        title="Accidents by Day of Week and Hour of Day",
        labels={
            "hour_of_day": "Hour of Day",
            "day_of_week": "Day of Week (0=Monday)",
            "accident_count": "Accident Count"
        }
    )
    fig
    return


if __name__ == "__main__":
    app.run()

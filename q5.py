

import marimo

__generated_with = "0.13.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import plotly as pl
    import plotly.express as px
    import polars as pl
    return pl, px


@app.cell
def _(pl):

    NYC_data=pl.read_csv("data/NYC_Collisions.csv")

    NYC_data

    return (NYC_data,)


@app.cell
def _(NYC_data, pl):
    NYC_VEH = NYC_data.with_columns(
        pl.col("Vehicle Type").fill_null("Not Known")
    )
    NYC_VEH
    return (NYC_VEH,)


@app.cell
def _(NYC_VEH, pl):

    NYC_VEH_clean = NYC_VEH.with_columns(
        pl.col("Vehicle Type").fill_null("Unknown")
    )


    return (NYC_VEH_clean,)


@app.cell
def _(NYC_VEH_clean, pl):

    NYC_ACC = NYC_VEH_clean.with_columns(
        (pl.col("Persons Injured") + pl.col("Persons Killed")+ pl.col("Pedestrians Injured")+ pl.col("Pedestrians Killed")+ pl.col("Cyclists Injured")+ pl.col("Cyclists Killed")+ pl.col("Motorists Injured")+ pl.col("Motorists Killed"))
        .alias("Harm")
    )
    NYC_ACC

    return (NYC_ACC,)


@app.cell
def _(NYC_ACC, pl):

    vehicle_avg = NYC_ACC.group_by("Vehicle Type").agg(
        pl.col("Harm").mean().alias("Average Harm")
    )

    vehicle_avg
    return (vehicle_avg,)


@app.cell
def _(vehicle_avg):
    #Find AVG
    highest_avg = vehicle_avg.sort("Average Harm", descending=True).head(1)

    highest_avg
    return


@app.cell
def _(vehicle_avg):
    top10 = vehicle_avg.sort("Average Harm", descending=True).head(10)
    top10
    return (top10,)


@app.cell
def _(px, top10):
    bar = px.bar(
        top10,
        x="Vehicle Type",
        y="Average Harm",
        title="Average Harm per Vehicle Type",
        labels={"Vehicle Type": "Vehicle Type", "Average Harm": "Average Injuries + Fatalities"},
    
    )
    bar
    return


if __name__ == "__main__":
    app.run()

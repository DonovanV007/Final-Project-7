

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
    NYC= pl.read_csv("data/NYC_Collisions.csv")


    NYC_Factor = NYC.with_columns(
        pl.col("Contributing Factor").fill_null("Not Known")
    )
    NYC_Factor

    return (NYC_Factor,)


@app.cell
def _(NYC_Factor):

    most_common_factor = (
        NYC_Factor.group_by("Contributing Factor")
          .len()
          .sort("len", descending=True)
          .select("Contributing Factor")
    )
    most_common_factor


    return


@app.cell
def _(NYC_Factor, pl):

    fatal_accidents = NYC_Factor.filter(pl.col("Persons Killed") > 0)


    most_common_fatal_factor = (
        fatal_accidents.group_by("Contributing Factor")
                       .len()
                       .sort("len", descending=True)
                       .select("Contributing Factor")
    )
    most_common_fatal_factor

    return


@app.cell
def _(NYC_Factor, pl):

    factor_counts = (
        NYC_Factor.group_by("Contributing Factor")
          .agg(pl.count().alias("counts"))  
          .sort("counts", descending=True)
        .head(5)
    )

    # Step 4: Convert for plotting
    factors = factor_counts["Contributing Factor"].to_list()
    counts = factor_counts["counts"].to_list()

    factor_counts


    return counts, factors


@app.cell
def _(counts, factors, px):

    pie_fig = px.pie(
        names=factors,
        values=counts,
        title="Distribution of Contributing Factors"
    )
    pie_fig



    return


@app.cell
def _(counts, factors, px):

    bar_fig = px.bar(
        x=factors,
        y=counts,
        title="Distribution of Contributing Factors",
        labels={'x': 'Contributing Factor', 'y': 'Number of Accidents'}
    )

    bar_fig
    return


if __name__ == "__main__":
    app.run()

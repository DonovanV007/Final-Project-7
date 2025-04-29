

import marimo

__generated_with = "0.13.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import plotly.express as px
    return pl, px


@app.cell
def _(pl):
    NYC = pl.read_csv("data/NYC_Collisions.csv")

    street_counts = (
        NYC.group_by("Street Name")
           .agg(pl.len().alias("accident_count"))
           .sort("accident_count", descending=True)
    )
    street_counts
    return NYC, street_counts


@app.cell
def _(NYC, street_counts):
    top_street = street_counts[0, "Street Name"]
    top_street_count = street_counts[0, "accident_count"]

    total_accidents = NYC.height
    percentage = (top_street_count / total_accidents) * 100
    print(f"The street with the most accidents is '{top_street}', with {top_street_count} accidents.")
    print(f"This represents {percentage:.2f}% of all reported accidents.")
    return


@app.cell
def _(px, street_counts):
    top_10_streets = street_counts.head(10)
    fig = px.bar(
        top_10_streets.to_dict(as_series=False),
        x="Street Name",
        y="accident_count",
        title="Top 10 Streets with Most Accidents",
        labels={"Street Name": "Street Name", "accident_count": "Number of Accidents"},
    )
    fig
    #bar
    return


if __name__ == "__main__":
    app.run()

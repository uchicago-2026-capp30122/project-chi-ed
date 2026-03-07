"""Helper functions for spatial maps and altair plots"""

import altair as alt
import pandas
import pathlib

def plot_bar_graph(df: pandas.DataFrame, variables: dict[str, str], school1: str, school2: str,
                   nrows: int, ncols: int, year: int = None, filepath: pathlib.Path = None):
    """Plot a grid of bar plots (nrows x ncols), one for each variable,
    highlighting the values for school1 and school2."""
    dataset = df.copy()
    if year is not None:
        dataset = dataset[dataset["year"] == year]

    charts = []
    school1_missing_vars = []
    school2_missing_vars = []

    N = dataset["school_name"].nunique()
    other_label = f"Other Chicago High Schools (N = {N})"

    def assign_highlight(scool_name: str, s1: str, s2: str, s1_label: str, s2_label: str, other_label: str) -> str:
        if scool_name == s1:
            return s1_label
        elif scool_name == s2:
            return s2_label
        return other_label

    for variable, varname in variables.items():
        data = dataset.copy()
        data[variable] = pandas.to_numeric(data[variable], errors="coerce")

        stat1_missing = data.loc[data["school_name"] == school1, variable].isna().all()
        stat2_missing = data.loc[data["school_name"] == school2, variable].isna().all()

        if stat1_missing:
            school1_missing_vars.append(varname)
        if stat2_missing:
            school2_missing_vars.append(varname)

        data = data.dropna(subset=[variable])

        school1_label = f"{school1} *" if stat1_missing else school1
        school2_label = f"{school2} *" if stat2_missing else school2

        # Assign highlight text
        data["highlight"] = data["school_name"].apply(assign_highlight, 
                                s1 = school1, s2 = school2, s1_label = school1_label, 
                                s2_label = school2_label, other_label = other_label)

        # Assign highlight color
        color_scale = alt.Scale(
            domain = [school1_label, school2_label, other_label],
            range = ["blue", "red", "lightgray"]
        )

        chart = (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x = alt.X("school_name:N", sort = alt.SortField(variable), axis = None),
                y = alt.Y(f"{variable}:Q", title = "",
                          axis = alt.Axis(grid = True, gridColor = "#e8e8e8", gridOpacity = 0.4)),
                color = alt.Color("highlight:N", scale = color_scale,
                                  legend = alt.Legend(title = None, orient = "top-left",
                                                     labelFontSize = 13, labelLimit = 400)),
            )
            .properties(width = 900 // ncols, height = 900 // nrows, title = varname)
        )
        charts.append(chart)

    # Dynamically arrange into grid. I am being overly cautious here 
    rows = []
    for index in range(nrows):
        row_charts = charts[index * ncols : (index + 1) * ncols]
        if row_charts:
            rows.append(alt.hconcat(*row_charts))

    grid = alt.vconcat(*rows)

    # Build a single subtitle for all missing values
    subtitles = []

    if school1_missing_vars:
        subtitles.append(f"* {school1} has missing values for {', '.join(school1_missing_vars)}")
    if school2_missing_vars:
        subtitles.append(f"* {school2} has missing values for {', '.join(school2_missing_vars)}")

    subtitle = subtitles if subtitles else alt.Undefined

    grid = grid.properties(title = alt.Title(text = "", subtitle = subtitle))

    if filepath is not None:
        grid.save(filepath, scale_factor = 2)
    else:
        raise Warning("No filepath provided. Remeber to provide a filepath to save the plot.")

    return filepath


def plot_time_series(df: pandas.DataFrame, variables: dict[str, str], school1: str, school2: str,
                     filepath: pathlib.Path = None):
    """Plot a 2x2 grid of line plots showing school1 and school2 trends from 2019 to 2025."""
    dataset = df.copy()
    dataset = dataset[dataset["school_name"].isin([school1, school2])]
    dataset["year"] = pandas.to_numeric(dataset["year"], errors="coerce")
    dataset = dataset.dropna(subset=["year"])
    dataset = dataset.sort_values("year")

    charts = []
    school1_missing_vars = []
    school2_missing_vars = []

    color_scale = alt.Scale(
        domain=[school1, school2],
        range=["blue", "red"]
    )

    for variable, varname in variables.items():
        data = dataset.copy()
        data[variable] = pandas.to_numeric(data[variable], errors="coerce")

        stat1_missing = data.loc[data["school_name"] == school1, variable].isna().all()
        stat2_missing = data.loc[data["school_name"] == school2, variable].isna().all()

        if stat1_missing:
            school1_missing_vars.append(varname)
        if stat2_missing:
            school2_missing_vars.append(varname)

        data = data.dropna(subset = [variable])

        chart = (
            alt.Chart(data)
            .mark_line(point = alt.OverlayMarkDef(size = 10))
            .encode(
                x = alt.X("year:O", title = "", axis = alt.Axis(labelAngle = 0)),
                y = alt.Y(f"{variable}:Q", title = "",
                         axis = alt.Axis(grid = True, gridColor = "#e8e8e8", gridOpacity = 0.4)),
                color=alt.Color("school_name:N", scale = color_scale,
                                legend = alt.Legend(title = None, orient = "top",
                                                  direction = "horizontal",
                                                  symbolType = "stroke",
                                                  labelFontSize = 14, labelLimit = 400
                                )),
            )
            .properties(width = 400, height = 220, title=varname)
        )
        charts.append(chart)

    grid = alt.vconcat(
        alt.hconcat(charts[0], charts[1]),
        alt.hconcat(charts[2], charts[3])
    )

    subtitles = []
    if school1_missing_vars:
        subtitles.append(f"* {school1} has missing values for {', '.join(school1_missing_vars)}")
    if school2_missing_vars:
        subtitles.append(f"* {school2} has missing values for {', '.join(school2_missing_vars)}")

    subtitle = subtitles if subtitles else alt.Undefined
    grid = grid.properties(title=alt.Title(text="", subtitle=subtitle))

    if filepath is not None:
        grid.save(filepath, scale_factor=2)
    else:
        raise Warning("No filepath provided. Remember to provide a filepath to save the plot.")

    return filepath

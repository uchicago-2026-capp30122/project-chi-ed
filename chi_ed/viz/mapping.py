"""Helper functions for spatial maps, and matplotlib plots"""

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas
import pathlib


OUTPUTS_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "outputs" 


def plot_bar_graph(data: pandas.DataFrame, variable: str, school1: str, school2: str, title: str):
    """This is a semi-comparative which will show the distribution of `variable` for all schools,
    but highlight the values for `school1` and `school2`."""
    # I am sorting the data for bars in increasing order  
    data[variable] = pandas.to_numeric(data[variable], errors = "coerce")
    data = data.sort_values(by=variable, ascending = True).reset_index(drop = True)
    schools = data["school_name"]
    values = data[variable]
    N = len(data[data[variable].notna()])

    # Assign colors: blue for school1, red for school2, gray for the rest
    color_map = {school1: "blue", school2: "red"}
    colors = [color_map.get(name, "lightgray") for name in schools]

    fig, ax = plt.subplots(figsize = (14, 7))
    bar_plot = ax.bar(range(len(values)), values, color = colors)

    legend_handles = [
        Patch(color = "blue", label = school1),
        Patch(color = "red", label = school2),
        Patch(color = "lightgray", label = f"Other Chicago High Schools (N = {N})"),
    ]
    ax.legend(handles = legend_handles, loc = "upper left", title = None, framealpha = 0.9)

    ax.set_title("")
    ax.set_ylabel(title)
    ax.set_xticks([])

    # This will LATER be much more flexible to save figures at specific directories with a defined filename logic
    fig.savefig(OUTPUTS_DIRPATH / "figures" / "tests" / f"{title}.png")

    return fig

import pandas
import typing
from great_tables import GT, md
import pathlib


def compute_avgs(df: pandas.DataFrame, variables: typing.List[str]):
    """Compute the average of each variable in variables for all schools across Chicago"""
    data = df.copy()
    for var in variables:
        data[var] = pandas.to_numeric(data[var], errors="coerce")

    return {var: data[var].mean() for var in variables}


def format_statistic(value: float, variable: str, round_to: int = 2):
    """Format percentages and rounding. Decided to remove the percentages, might add them back in later."""
    rounded = round(value, round_to)
    if round_to == 0:
        rounded = int(rounded)
    return str(rounded)


def summary_table(
    df: pandas.DataFrame,
    section: str,
    variables: dict[str, str],
    school1: str,
    school2: str,
    filepath: pathlib.Path,
    round_to: int = 0,
    display_chicago: bool = True,
    year: int = 2025,
):
    """Create a summary table comparing both schools, with a Chicago average column if display_chicago is True."""
    data = df.loc[df["year"] == year].copy() if "year" in df.columns else df.copy()
    var_cols = [var for var in variables.keys() if var in data.columns]

    numeric_vars = []
    for var in var_cols:
        converted = pandas.to_numeric(data[var], errors="coerce")
        if converted.notna().any():
            data[var] = converted
            numeric_vars.append(var)

    chicago_avgs = compute_avgs(data, numeric_vars)

    # Display the school names with a maximum of 4 words if they are too long
    # This is a hack to make the table flexible and readable regardless of the length of the text
    school1_display = " ".join(school1.split()[:4]) if len(school1) > 35 else school1
    school2_display = " ".join(school2.split()[:4]) if len(school2) > 35 else school2

    rows = []
    for var, display_name in variables.items():
        if var not in data.columns:
            rows.append(
                {
                    "Metric": display_name,
                    school1_display: "",
                    school2_display: "",
                    "Chicago Avg.": "",
                }
            )
            continue

        val_school1 = data.loc[data["school_name"] == school1, var]
        val_school2 = data.loc[data["school_name"] == school2, var]

        # Check if the variable is numeric, we will not compute averages for non-numeric variables
        is_numeric = var in numeric_vars

        if is_numeric:
            stat1_str = (
                format_statistic(val_school1.iloc[0], var, round_to)
                if len(val_school1) and pandas.notna(val_school1.iloc[0])
                else ""
            )
            stat2_str = (
                format_statistic(val_school2.iloc[0], var, round_to)
                if len(val_school2) and pandas.notna(val_school2.iloc[0])
                else ""
            )
            if display_chicago:
                avg_str = (
                    format_statistic(chicago_avgs[var], var, round_to)
                    if var in chicago_avgs
                    else ""
                )
        else:
            # For non-numeric variables, we will just display the comparison between the two schools
            stat1_str = (
                str(val_school1.iloc[0])
                if len(val_school1) and pandas.notna(val_school1.iloc[0])
                else ""
            )
            stat2_str = (
                str(val_school2.iloc[0])
                if len(val_school2) and pandas.notna(val_school2.iloc[0])
                else ""
            )
            if display_chicago:
                avg_str = ""

        stats = {
            "Metric": display_name,
            school1_display: stat1_str if stat1_str else "",
            school2_display: stat2_str if stat2_str else "",
        }

        # Add the Chicago average if specified
        if display_chicago:
            stats["Chicago Avg."] = avg_str

        rows.append(stats)

    table = (
        GT(pandas.DataFrame(rows))
        .tab_header(title=f"{section}")
        .tab_source_note("Empty cells indicates missing statistics.")
    )

    # Save to tex file, but just in case I forget to pass the correct path then default to png
    filepath = pathlib.Path(filepath)
    if filepath.suffix == ".tex":
        latex_table = table.as_latex()
        latex_table = latex_table.replace("\\begin{table}[!t]", "\\begin{table}[H]")
        latex_table = latex_table.replace(
            "\\begin{table}[H]",
            "\\begin{table}[H]\n\\renewcommand{\\arraystretch}{1.5}",
        )
        latex_table = latex_table.replace(
            "\\fontsize{12.0pt}{14.4pt}", "\\fontsize{10pt}{11pt}"
        )
        # This is a hack to force the table to center allign statistics in each column
        for old, new in [
            ("lrrr}", "lccc}"),
            ("lrr}", "lcc}"),
            ("llll}", "lccc}"),
            ("lll}", "lcc}"),
        ]:
            latex_table = latex_table.replace(old, new)
        with open(filepath, "w") as f:
            f.write(latex_table)
    else:
        table.save(str(filepath))

    return table

import pandas
import typing
from great_tables import GT, md
import pathlib


def compute_avgs(df: pandas.DataFrame, variables: typing.List[str]):
    """Compute the average of the variables for all schools."""
    data = df.copy()
    for var in variables:
        data[var] = pandas.to_numeric(data[var], errors="coerce")

    return {var: data[var].mean() for var in variables}


def format_statistic(value: float, variable: str, round_to: int = 2):
    """Format percentages and rates as actual percentages"""
    rounded = round(value * 100, round_to) if variable in variables_in_perc else round(value, round_to)
    if round_to == 0:
        rounded = int(rounded)
    return f"{rounded}%" if variable in variables_in_perc else f"{rounded}"


def summary_table(df: pandas.DataFrame, section: str, variables: dict[str, str], 
                  school1: str, school2: str, filepath: pathlib.Path, round_to: int = 0,
                  display_chicago: bool = True):
    """Create a summary table comparing both schools with a Chicago average column."""
    data = df.copy()
    var_cols = [v for v in variables.keys() if v in data.columns]

    numeric_vars = []
    for var in var_cols:
        converted = pandas.to_numeric(data[var], errors="coerce")
        if converted.notna().any():
            data[var] = converted
            numeric_vars.append(var)

    chicago_avgs = compute_avgs(data, numeric_vars)

    rows = []
    for var, display_name in variables.items():
        if var not in data.columns:
            rows.append({"Variable": display_name, school1: "", school2: "", "Chicago Avg.": ""})
            continue

        val_school1 = data.loc[data["school_name"] == school1, var]
        val_school2 = data.loc[data["school_name"] == school2, var]

        is_numeric = var in numeric_vars

        if is_numeric:
            stat1_str = format_statistic(val_school1.iloc[0], var, round_to) if len(val_school1) and val_school1.notna().any() else ""
            stat2_str = format_statistic(val_school2.iloc[0], var, round_to) if len(val_school2) and val_school2.notna().any() else ""
            if display_chicago:
                avg_str = format_statistic(chicago_avgs[var], var, round_to) if var in chicago_avgs else ""
        else:
            stat1_str = str(val_school1.iloc[0]) if len(val_school1) and val_school1.notna().any() else ""
            stat2_str = str(val_school2.iloc[0]) if len(val_school2) and val_school2.notna().any() else ""
            if display_chicago:
                avg_str = ""

        stats = {
            "Variable": display_name,
            school1: stat1_str,
            school2: stat2_str
        }

        # Add the Chicago average specified
        if display_chicago:
            stats["Chicago Avg."] = avg_str

        rows.append(stats)

    table = (
        GT(pandas.DataFrame(rows))
        .tab_header(title = f"{section} Summary Statistics")
        .tab_source_note("Empty cells indicates missing statistics.")
    )

    # Save to tex file, but just in case I forget to pass the correct path the  default to png
    filepath = pathlib.Path(filepath)
    if filepath.suffix == ".tex":
        latex_str = table.as_latex()
        latex_str = latex_str.replace("\\begin{table}[!t]", "\\begin{table}[H]")
        latex_str = latex_str.replace("\\begin{table}[H]", "\\begin{table}[H]\n\\renewcommand{\\arraystretch}{1.5}")
        latex_str = latex_str.replace("\\fontsize{12.0pt}{14.4pt}", "\\fontsize{10pt}{11pt}")
        for old, new in [("lrrr}", "lccc}"), ("lrr}", "lcc}"), ("llll}", "lccc}"), ("lll}", "lcc}")]:
            latex_str = latex_str.replace(old, new)
        with open(filepath, "w") as f:
            f.write(latex_str)
    else:
        table.save(str(filepath))

    return table



# I might not need this
variables_in_perc = []
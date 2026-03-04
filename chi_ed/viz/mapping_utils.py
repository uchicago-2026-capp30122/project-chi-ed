"""Helper functions for spatial maps and altair plots"""

import altair as alt
import pandas
import pathlib
import typing
from great_tables import GT, md


OUTPUTS_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "outputs" 


def plot_bar_graph(data: pandas.DataFrame, variable: str, school1: str, school2: str, filename: str = None):
    """This is a semi-comparative which will show the distribution of `variable` for all schools,
    but highlight the values for `school1` and `school2`."""
    data = data.copy()
    data[variable] = pandas.to_numeric(data[variable], errors = "coerce")

    # Check which highlighted schools have missing values before dropping NAs
    school1_missing = data.loc[data["school_name"] == school1, variable].isna().all()
    school2_missing = data.loc[data["school_name"] == school2, variable].isna().all()

    data = data.dropna(subset = [variable])
    N = len(data)

    # Build legend labels, appending a footnote marker if missing
    school1_label = f"{school1} *" if school1_missing else school1
    school2_label = f"{school2} *" if school2_missing else school2
    other_label = f"Other Chicago High Schools (N = {N})"

    def assign_highlight(name):
        if name == school1:
            return school1_label
        elif name == school2:
            return school2_label
        return other_label

    data["highlight"] = data["school_name"].apply(assign_highlight)

    color_scale = alt.Scale(
        domain = [school1_label, school2_label, other_label],
        range = ["blue", "red", "lightgray"]
    )

    # Build footnote for missing values
    missing_names = []
    if school1_missing:
        missing_names.append(school1)
    if school2_missing:
        missing_names.append(school2)

    subtitle = f"* {', '.join(missing_names)}: missing value for this variable" if missing_names else ""

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x = alt.X("school_name:N", sort = alt.SortField(variable), axis = None),
            y = alt.Y(f"{variable}:Q", title = varname_mapping.get(variable, variable)),
            color = alt.Color("highlight:N", scale = color_scale, legend = alt.Legend(title = None)),
        )
        .properties(width = 700, height = 350, title = alt.Title(text = "", subtitle = subtitle))
    )
    if filename is not None:
        chart.save(filename, scale_factor = 2)

    return chart


def compute_avgs(data: pandas.DataFrame, variables: typing.List[str]):
    """This function will compute the average of the variables for all schools."""
    df = data.copy()
    df[variables] = pandas.to_numeric(df[variables], errors = "coerce")
    df = df.dropna(subset = variables)

    return {var: df[var].mean() for var in variables}


def format_statistic(value: float, variable: str):
    """This function will format percentages and rates as actual percentages"""
    if variable in variables_in_perc:
        return f"{value * 100:.2f}%"
    else:
        return f"{value:.2f}"


def summary_table(data: pandas.DataFrame, variables: typing.List[str], school1: str, school2: str, filename: str):
    """This function will create a summary table of the variables both schools, 
    adding a 3rd column for the overall average."""
    df = data.copy()
    for var in variables:
        df[var] = pandas.to_numeric(df[var], errors = "coerce")

    chicago_avgs = compute_avgs(df, variables)

    rows = []
    for var in variables:
        val_school1 = df.loc[df["school_name"] == school1, var]
        val_school2 = df.loc[df["school_name"] == school2, var]

        s1_str = format_statistic(val_school1.iloc[0], var) if len(val_school1) and val_school1.notna().any() else ""
        s2_str = format_statistic(val_school2.iloc[0], var) if len(val_school2) and val_school2.notna().any() else ""
        avg_str = format_statistic(chicago_avgs[var], var) if var in chicago_avgs else ""

        rows.append({
            "Variable": varname_mapping.get(var, var),
            school1: s1_str,
            school2: s2_str,
            "Chicago Avg.": avg_str
        })

    table_df = pandas.DataFrame(rows)

    table = (
        GT(table_df)
        .tab_header(title = "Summary Statistics for Key Variables")
        .tab_source_note("Empty cell indicates missing statistic for the corresponding school.")
    )
    table.save(filename)

    return table



comparition_type_mapping = {
    "barplot": [
        "math_proficiency", 
        "ELA_proficiency", 
        "science_proficiency", 
        "grad_rate", 
        "pp_expenditure"
    ],
    "table": [
        "perc_novice_teachers", 
        "avg_teaching_exp", 
        "pupil_teacher_ratio", 
        "avg_class_size", 
        "chronic_absenteeism", 
        "dropout_rate", 
        "enrollment", 
        "num_children_with_disabilities", 
        "teacher_attendance_rate"
    ]
}

varname_mapping = {
    "math_proficiency": "Math Proficiency",
    "ELA_proficiency": "ELA Proficiency",
    "science_proficiency": "Science Proficiency",
    "grad_rate": "Graduation Rate",
    "pp_expenditure": "Instructional Expenditure per Pupil",
    "perc_novice_teachers": "Percentage of Novice Teachers",
    "avg_teaching_exp": "Average Teaching Experience",
    "pupil_teacher_ratio": "Pupil Teacher Ratio",
    "avg_class_size": "Average Class Size",
    "chronic_absenteeism": "Chronic Absenteeism",
}

variables_in_perc = [
    "math_proficiency",
    "ELA_proficiency",
    "science_proficiency",
    "grad_rate",
    "perc_novice_teachers",
    "teacher_attendance_rate"
]
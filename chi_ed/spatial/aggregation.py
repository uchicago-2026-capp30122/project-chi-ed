import pandas as pd

CHOROPLETH_METRICS = [
    "ELA_proficiency",
    "math_proficiency",
    "graduation_rate",
    "college_enrollment_rate",
    "attendance_rate_current_year",
    "chronic_absenteeism",
    "sat_school_average",
]

COMPARISON_METRICS = CHOROPLETH_METRICS + [
    "enrollment",
    "avg_class_size",
    "avg_teaching_exp",
    "perc_novice_teachers",
    "teacher_attendance_rate",
    "student_count_low_income",
    "student_count_special_education",
    "student_count_black",
    "student_count_hispanic",
    "student_count_white",
    "student_count_asian",
]


def aggregate_by_neighborhood(schools, metric, year):
    """
    Aggregate a metric by neighborhood for a given year.

    The mean is computed over available schools data only.
    A school_count column is included so users can know how many schools
    contributed to each neighborhood's average.

    Parameters:
        schools: DataFrame filtered to a single year.
        metric: Column name to aggregate.
        year: School year being aggregated (used for labeling only).

    Returns:
        DataFrame with columns [neighborhood, {metric}, school_count, year].
    """
    agg = schools.groupby("neighborhood")[metric].agg(["mean", "count"]).reset_index()
    agg.columns = ["neighborhood", metric, "school_count"]
    agg["year"] = year
    return agg

def get_available_metrics(schools, metrics):
    """
    Return only metrics that have at least some data for the given schools DataFrame.

    Parameters:
        schools: DataFrame filtered to a single year.
        metrics: List of metric column names to check.

    Returns:
        List of metrics with at least one non-null value.
    """
    return [metric for metric in metrics if metric in schools.columns and schools[metric].notna().any()]


def get_school_comparison(schools, school_a, school_b):
    """
    Extract and compare all comparison metrics for two schools side by side.

    Parameters:
        schools: DataFrame filtered to a single year.
        school_a: Name of the first school.
        school_b: Name of the second school.

    Returns:
        DataFrame with columns [metric, school_a, school_b].
    """
    available_metrics = get_available_metrics(schools, COMPARISON_METRICS)

    a = schools[schools["school_name"] == school_a][available_metrics].iloc[0]
    b = schools[schools["school_name"] == school_b][available_metrics].iloc[0]

    comparison = pd.DataFrame({
        "metric": available_metrics,
        school_a: a.values,
        school_b: b.values,
    })

    return comparison
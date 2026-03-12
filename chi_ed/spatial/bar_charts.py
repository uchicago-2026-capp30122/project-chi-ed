import json
import plotly.graph_objects as go
from .aggregation import aggregate_by_neighborhood, get_school_comparison
from .data import ROOT


with open(ROOT / "data" / "clean" / "variables.json") as f:
    METRIC_LABELS = json.load(f)

# Description of the metrics to appear as part of the dashboard
METRIC_DESCRIPTIONS = {
    "graduation_rate": "Average graduation rate across schools in each neighborhood",
    "sat_school_average": "Average SAT score across schools in each neighborhood",
    "college_enrollment_rate": "Average % of students enrolling in college after graduation",
    "attendance_rate_current_year": "Average student attendance rate across schools",
    "ELA_proficiency": "Average % of students meeting ELA proficiency standards",
    "math_proficiency": "Average % of students meeting math proficiency standards",
    "science_proficiency": "Average % of students meeting science proficiency standards",
    "chronic_absenteeism": "Average % of students chronically absent across schools",
}

# Metrics to display in school comparison chart
SCHOOL_COMPARISON_METRICS = [
    "ELA_proficiency",
    "math_proficiency",
    "graduation_rate",
    "college_enrollment_rate",
    "attendance_rate_current_year",
    "chronic_absenteeism",
    "sat_school_average",
    "enrollment",
    "avg_class_size",
]


def make_bar_chart(neighborhoods, metric, color, metric_max):
    """
    Making a horizontal bar chart for a set of neighborhoods.

    Parameters:
        neighborhoods: Data frame of neighborhoods with aggregated metric values
        metric: Metric to plot
        color: Bar color

    Returns:
        A plotly bar chart
    """
    # Documentation used: https://plotly.com/python/bar-charts/
    fig = go.Figure(
        go.Bar(
            x=neighborhoods[metric],
            y=neighborhoods["neighborhood"],
            orientation="h",
            marker_color=color,
            text=neighborhoods[metric].round(1),
            textposition="outside",
            hoverinfo="none",
        )
    )

    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="DM Sans, sans-serif", color="#1a1814"),
        margin=dict(l=150, r=60, t=10, b=0),
        showlegend=False,
    )
    fig.update_xaxes(showgrid=False, range=[0, metric_max * 1.15])
    fig.update_yaxes(
        showgrid=False,
        tickfont=dict(family="DM Sans, sans-serif", color="#1a1814", size=11),
        ticksuffix="  ",
    )

    return fig


def make_neighborhood_performance_charts(schools, metric, year):
    """
    Build two bar charts showing top 10 and bottom 10 neighborhoods by metric.

    Parameters:
        schools: Data frame containing panel data of schools
        metric: Metric to aggregate and rank neighborhoods by
        year: Year to filter school data by

    Returns:
        top_performing_chart: A plotly bar graph for top 10 neighborhoods
        worst_performing_chart: A plotly bar chart for bottom 10 neighborhoods
        neighborhoods_no_data: List of neighborhood names with no data
                               for this metric (if any exist)
        metric_description: Description of the metric for display in the dashboard
    """
    neighborhood_aggregation = aggregate_by_neighborhood(schools, metric, year)

    # Splitting the schools data frame into two categories
    # 1. Neighborhoods with data
    # 2. Neighborhoods without data
    neighborhoods_with_data = neighborhood_aggregation.dropna(subset=[metric])
    neighborhoods_no_data = neighborhood_aggregation[
        neighborhood_aggregation[metric].isna()
    ]["neighborhood"].tolist()

    # Top 10 best performing neighborhoods — sorted in descending order
    top_performing_neighborhoods = neighborhoods_with_data.nlargest(
        10, metric
    ).sort_values(metric, ascending=True)

    # Top 10 least performing neighborhoods
    # Neighborhoods with worst performance at the top
    worst_performing_neighborhoods = neighborhoods_with_data.nsmallest(
        10, metric
    ).sort_values(metric, ascending=True)

    metric_description = METRIC_DESCRIPTIONS.get(
        metric,
        f"Average {metric.replace('_', ' ').title()} across schools in each neighborhood",
    )

    metric_max = neighborhoods_with_data[metric].max()

    top_performing_chart = make_bar_chart(
        top_performing_neighborhoods, metric, "#5ba3d4", metric_max
    )
    worst_performing_chart = make_bar_chart(
        worst_performing_neighborhoods, metric, "#c94f2c", metric_max
    )

    return (
        top_performing_chart,
        worst_performing_chart,
        neighborhoods_no_data,
        metric_description,
    )


def make_school_comparison_chart(schools, school_a, school_b):
    """
    Build a grouped bar chart comparing two schools across key metrics.

    Parameters:
        schools: Data frame containing school data filtered to a single year
        school_a: Name of the first school
        school_b: Name of the second school

    Returns:
        A plotly grouped bar chart
    """
    comparison = get_school_comparison(schools, school_a, school_b)

    # Filter to keep only the metrics we want to display
    comparison = comparison[comparison["metric"].isin(SCHOOL_COMPARISON_METRICS)]

    comparison["metric"] = comparison["metric"].map(METRIC_LABELS)

    # https://plotly.com/python/grouped-bar-charts/
    school_bar_graph = go.Figure()
    school_bar_graph.add_trace(
        go.Bar(
            name=school_a,
            x=comparison["metric"],
            y=comparison[school_a],
            marker_color="#5ba3d4",
            hovertemplate="%{x}: %{y}<extra></extra>",
        )
    )
    school_bar_graph.add_trace(
        go.Bar(
            name=school_b,
            x=comparison["metric"],
            y=comparison[school_b],
            marker_color="#c94f2c",
            hovertemplate="%{x}: %{y}<extra></extra>",
        )
    )

    school_bar_graph.update_layout(
        barmode="group",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="DM Sans, sans-serif", color="#1a1814"),
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            font=dict(family="DM Sans, sans-serif", size=11),
        ),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(family="DM Mono, monospace", size=10, color="#6b6560"),
        ),
    )
    school_bar_graph.update_xaxes(showgrid=False)
    school_bar_graph.update_yaxes(showgrid=False)

    return school_bar_graph

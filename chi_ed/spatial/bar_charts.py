import plotly.graph_objects as go
from .aggregation import aggregate_by_neighborhood

# Human-readable descriptions for each metric
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


def make_bar_chart(neighborhoods, metric, color):
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
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        showgrid=False,
        tickfont=dict(family="DM Sans, sans-serif", color="#1a1814", size=11),
        ticksuffix="  "
    )

    return fig


def make_neighborhood_performance_charts(schools, metric, year):
    """
    Build two bar charts showing top 10 and bottom 10 neighborhoods by metric.

    Parameters:
        schools: A data frame filtered to a single year containing mappable schools only
        metric: Metric to aggregate and rank neighborhoods by
        year: Year to filter school data by

    Returns:
        top_performing_chart: Plotly figure for top 10 neighborhoods
        worst_performing_chart: Plotly figure for bottom 10 neighborhoods
        neighborhoods_no_data: List of neighborhood names with no data for this metric
        metric_description: Human-readable description of the metric
    """
    neighborhood_aggregation = aggregate_by_neighborhood(schools, metric, year)

    # Splitting the schools data frame into two categories
    # 1. Neighborhoods with data
    # 2. Neighborhoods without data
    neighborhoods_with_data = neighborhood_aggregation.dropna(subset=[metric])
    neighborhoods_no_data = neighborhood_aggregation[
        neighborhood_aggregation[metric].isna()
    ]["neighborhood"].tolist()

    # Top 10 best performing neighborhoods — highest value at top
    top_performing_neighborhoods = neighborhoods_with_data.nlargest(
        10, metric
    ).sort_values(metric, ascending=True)

    # Top 10 worst performing neighborhoods — lowest value at top
    worst_performing_neighborhoods = neighborhoods_with_data.nsmallest(
        10, metric
    ).sort_values(metric, ascending=True)

    metric_description = METRIC_DESCRIPTIONS.get(
        metric, f"Average {metric.replace('_', ' ').title()} across schools in each neighborhood"
    )

    top_performing_chart = make_bar_chart(top_performing_neighborhoods, metric, "#5ba3d4")
    worst_performing_chart = make_bar_chart(worst_performing_neighborhoods, metric, "#c94f2c")

    return top_performing_chart, worst_performing_chart, neighborhoods_no_data, metric_description
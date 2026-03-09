import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
from .data import load_schools, get_mappable_schools, get_available_years
from .base_map import make_base_map
from .bar_charts import (
    make_neighborhood_performance_charts,
    make_school_comparison_chart,
    METRIC_LABELS,
)
from .aggregation import (
    get_available_metrics,
    CHOROPLETH_METRICS,
)

# https://dash-bootstrap-components.opensource.faculty.ai/docs/quickstart/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

available_years = get_available_years()
school_data = load_schools()

# Shared title bar style matching mockup CSS variables
TITLE_BAR_STYLE = {
    "backgroundColor": "#f5f2ee",
    "padding": "10px 15px",
    "display": "flex",
    "justifyContent": "space-between",
    "alignItems": "flex-start",
    "borderBottom": "1px solid #ddd9d3",
}

# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
app.layout = dbc.Container(
    [
        # Title of the Dashboard
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Span(
                            "Chicago Public Schools — Neighborhood Explorer",
                            style={"fontWeight": "bold", "fontSize": "1.1rem"},
                        ),
                        html.Span(
                            "CAPP 30122 · PROJECT CHI-ED",
                            style={"fontSize": "0.85rem", "letterSpacing": "0.05em"},
                        ),
                    ],
                    style={
                        "backgroundColor": "#1a1a1a",
                        "color": "white",
                        "padding": "25px 25px",  # setting thickness of the title box
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "marginLeft": "-12px",  # reducing page margins
                        "marginRight": "-12px",
                    },
                ),
                width=12,
            ),
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Year"),
                        dcc.Slider(
                            id="year-dropdown",
                            min=available_years[0],
                            max=available_years[-1],
                            step=1,
                            value=available_years[-1],
                            marks={y: str(y) for y in available_years},
                        ),
                    ],
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/tabs/
        dbc.Tabs(
            id="tabs",
            active_tab="tab-neighborhood",
            children=[
                dbc.Tab(
                    label="Neighborhood View",
                    tab_id="tab-neighborhood",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Metric", className="mt-3"),
                                        dcc.Dropdown(
                                            id="metric-dropdown",
                                            value="graduation_rate",
                                            clearable=False,
                                        ),
                                    ],
                                    width=4,
                                ),
                            ],
                            className="my-2",
                        ),
                        dbc.Row(
                            [
                                # Header of the Chicago map
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Link(
                                                    rel="stylesheet",
                                                    href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap",
                                                ),
                                                html.Span(
                                                    "Chicago Neighborhoods",
                                                    style={
                                                        "fontFamily": "'DM Serif Display', serif",
                                                        "fontSize": "0.95rem",
                                                        "color": "#1a1814",
                                                        "fontWeight": "bold",
                                                    },
                                                ),
                                                html.Span(
                                                    "Click neighborhood to zoom  ·  Hover school to view details",
                                                    style={
                                                        "fontFamily": "'DM Mono', monospace",
                                                        "fontSize": "0.7rem",
                                                        "color": "#6b6560",
                                                    },
                                                ),
                                            ],
                                            style={
                                                **TITLE_BAR_STYLE,
                                                "border": "1px solid #ddd9d3",
                                                "borderBottom": "1px solid #ddd9d3",
                                                "borderRadius": "4px 4px 0 0",
                                            },
                                        ),
                                        # https://dash.plotly.com/dash-html-components/iframe
                                        # https://python-visualization.github.io/folium/latest/advanced_guide/flask.html
                                        html.Iframe(
                                            id="base-map",
                                            style={
                                                "width": "100%",
                                                "height": "830px",
                                                "border": "1px solid #ddd9d3",
                                                "borderTop": "none",
                                                "borderRadius": "0 0 4px 4px",
                                            },
                                        ),
                                    ],
                                    width=5,
                                ),
                                # Right panel — with two stacked bar chart
                                # Top performing neighborhoods on top
                                # Low performing neighborhoods at the bottom
                                dbc.Col(
                                    [
                                        # Top performing neighborhoods
                                        dbc.Card(
                                            [
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.Span(
                                                                    id="top-chart-title",
                                                                    style={
                                                                        "fontFamily": "'DM Serif Display', serif",
                                                                        "fontSize": "0.95rem",
                                                                        "color": "#1a1814",
                                                                        "fontWeight": "bold",
                                                                    },
                                                                ),
                                                                html.Br(),
                                                                html.Span(
                                                                    id="top-chart-description",
                                                                    style={
                                                                        "fontFamily": "'DM Mono', monospace",
                                                                        "fontSize": "0.7rem",
                                                                        "color": "#6b6560",
                                                                    },
                                                                ),
                                                            ]
                                                        ),
                                                        html.Span(
                                                            id="top-chart-year",
                                                            style={
                                                                "fontFamily": "'DM Mono', monospace",
                                                                "fontSize": "0.7rem",
                                                                "color": "#6b6560",
                                                                "whiteSpace": "nowrap",
                                                            },
                                                        ),
                                                    ],
                                                    style=TITLE_BAR_STYLE,
                                                ),
                                                dcc.Graph(
                                                    id="top-performing-chart",
                                                    style={"height": "360px"},
                                                ),
                                            ],
                                            style={
                                                "border": "1px solid #ddd9d3",
                                                "borderRadius": "4px",
                                                "marginBottom": "12px",
                                            },
                                        ),
                                        # Least performing neighborhoods
                                        dbc.Card(
                                            [
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.Span(
                                                                    id="worst-chart-title",
                                                                    style={
                                                                        "fontFamily": "'DM Serif Display', serif",
                                                                        "fontSize": "0.95rem",
                                                                        "color": "#1a1814",
                                                                        "fontWeight": "bold",
                                                                    },
                                                                ),
                                                                html.Br(),
                                                                html.Span(
                                                                    id="worst-chart-description",
                                                                    style={
                                                                        "fontFamily": "'DM Mono', monospace",
                                                                        "fontSize": "0.7rem",
                                                                        "color": "#6b6560",
                                                                    },
                                                                ),
                                                            ]
                                                        ),
                                                        html.Span(
                                                            id="worst-chart-year",
                                                            style={
                                                                "fontFamily": "'DM Mono', monospace",
                                                                "fontSize": "0.7rem",
                                                                "color": "#6b6560",
                                                                "whiteSpace": "nowrap",
                                                            },
                                                        ),
                                                    ],
                                                    style=TITLE_BAR_STYLE,
                                                ),
                                                dcc.Graph(
                                                    id="worst-performing-chart",
                                                    style={"height": "360px"},
                                                ),
                                            ],
                                            style={
                                                "border": "1px solid #ddd9d3",
                                                "borderRadius": "4px",
                                            },
                                        ),
                                    ],
                                    width=7,
                                ),
                            ]
                        ),
                    ],
                ),
                # School comparison tab for dashboard
                dbc.Tab(
                    label="School Comparison",
                    tab_id="tab-comparison",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("School A", className="mt-3"),
                                        dcc.Dropdown(
                                            id="school-a-dropdown", clearable=False
                                        ),
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("School B", className="mt-3"),
                                        dcc.Dropdown(
                                            id="school-b-dropdown", clearable=False
                                        ),
                                    ],
                                    width=4,
                                ),
                            ],
                            className="my-2",
                        ),
                        # Header on top of the neighborhood map
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Span(
                                                    "Chicago Neighborhoods",
                                                    style={
                                                        "fontFamily": "'DM Serif Display', serif",
                                                        "fontSize": "0.95rem",
                                                        "color": "#1a1814",
                                                        "fontWeight": "bold",
                                                    },
                                                ),
                                                html.Span(
                                                    "Hover school to view details  ·  Select schools to compare",
                                                    style={
                                                        "fontFamily": "'DM Mono', monospace",
                                                        "fontSize": "0.7rem",
                                                        "color": "#6b6560",
                                                    },
                                                ),
                                            ],
                                            style={
                                                **TITLE_BAR_STYLE,
                                                "border": "1px solid #ddd9d3",
                                                "borderBottom": "1px solid #ddd9d3",
                                                "borderRadius": "4px 4px 0 0",
                                            },
                                        ),
                                        html.Iframe(
                                            id="comparison-map",
                                            style={
                                                "width": "100%",
                                                "height": "700px",
                                                "border": "1px solid #ddd9d3",
                                                "borderTop": "none",
                                                "borderRadius": "0 0 4px 4px",
                                            },
                                        ),
                                    ],
                                    width=5,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            html.Div(
                                                [
                                                    html.Span(
                                                        "School Comparison",
                                                        style={
                                                            "fontFamily": "'DM Serif Display', serif",
                                                            "fontSize": "0.95rem",
                                                            "color": "#1a1814",
                                                            "fontWeight": "bold",
                                                        },
                                                    ),
                                                ],
                                                style=TITLE_BAR_STYLE,
                                            ),
                                            dcc.Graph(
                                                id="comparison-chart",
                                                style={
                                                    "height": "700px",
                                                    "padding": "10px",
                                                },
                                            ),
                                        ],
                                        style={
                                            "border": "1px solid #ddd9d3",
                                            "borderRadius": "4px",
                                        },
                                    ),
                                    width=7,
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        ),
    ],
    fluid=True,
    style={"paddingBottom": "80px"},
)


# Updating metric dropdown options based on selected year
@callback(
    Output("metric-dropdown", "options"),
    Output("metric-dropdown", "value"),
    Input("year-dropdown", "value"),
)
def update_metric_options(year):
    schools = get_mappable_schools(school_data[school_data["year"] == year])
    available = get_available_metrics(schools, CHOROPLETH_METRICS)
    options = [
        {"label": METRIC_LABELS.get(m, m.replace("_", " ").title()), "value": m}
        for m in available
    ]
    return options, available[0] if available else None


# Updating neighborhood level map when year or metric changes
@callback(
    Output("base-map", "srcDoc"),
    Input("year-dropdown", "value"),
    Input("metric-dropdown", "value"),
)
def update_map(year, metric):
    return make_base_map(year, metric)._repr_html_()


# Updating bar charts for top and worst performing neighborhoods
@callback(
    Output("top-performing-chart", "figure"),
    Output("worst-performing-chart", "figure"),
    Output("top-chart-title", "children"),
    Output("worst-chart-title", "children"),
    Output("top-chart-description", "children"),
    Output("worst-chart-description", "children"),
    Output("top-chart-year", "children"),
    Output("worst-chart-year", "children"),
    Input("year-dropdown", "value"),
    Input("metric-dropdown", "value"),
)
def update_bar_charts(year, metric):
    schools = get_mappable_schools(school_data[school_data["year"] == year])
    top_chart, worst_chart, _, metric_description = (
        make_neighborhood_performance_charts(schools, metric, year)
    )

    metric_label = METRIC_LABELS.get(metric, metric.replace("_", " ").title())
    year_label = f"{year}  ·  Average across schools"

    return (
        top_chart,
        worst_chart,
        f"Top Performing Neighborhoods — {metric_label}",
        f"Low Performing Neighborhoods — {metric_label}",
        metric_description,
        metric_description,
        year_label,
        year_label,
    )


# Populating school dropdowns when user changes year
@callback(
    Output("school-a-dropdown", "options"),
    Output("school-b-dropdown", "options"),
    Output("school-a-dropdown", "value"),
    Output("school-b-dropdown", "value"),
    Input("year-dropdown", "value"),
)
def update_school_dropdowns(year):
    schools = get_mappable_schools(school_data[school_data["year"] == year])
    school_names = sorted(schools["school_name"].dropna().unique())
    options = [{"label": s, "value": s} for s in school_names]
    return options, options, options[0]["value"], options[1]["value"]


# Update comparison map when year changes — no metric, shows base light blue fill
@callback(
    Output("comparison-map", "srcDoc"),
    Input("year-dropdown", "value"),
)
def update_comparison_map(year):
    return make_base_map(year)._repr_html_()


# Update comparison chart when schools or year changes
@callback(
    Output("comparison-chart", "figure"),
    Input("year-dropdown", "value"),
    Input("school-a-dropdown", "value"),
    Input("school-b-dropdown", "value"),
)
def update_comparison_chart(year, school_a, school_b):
    if not school_a or not school_b:
        return {}

    schools = school_data[school_data["year"] == year]
    return make_school_comparison_chart(schools, school_a, school_b)


if __name__ == "__main__":
    print("I AM RUNNING")
    app.run(debug=True)

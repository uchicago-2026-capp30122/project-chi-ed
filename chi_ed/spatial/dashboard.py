import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from .data import load_schools, get_mappable_schools, get_available_years
from .base_map import make_base_map
from .aggregation import get_available_metrics, aggregate_by_neighborhood, get_school_comparison, CHOROPLETH_METRICS

# https://dash-bootstrap-components.opensource.faculty.ai/docs/quickstart/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

available_years = get_available_years()
school_data = load_schools()

# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
app.layout = dbc.Container([

    dbc.Row(
    dbc.Col(
        html.Div([
            html.Span("Chicago Public Schools — Neighborhood Explorer", style={"fontWeight": "bold", "fontSize": "1.1rem"}),
            html.Span("CAPP 30122 · PROJECT CHI-ED", style={"fontSize": "0.85rem", "letterSpacing": "0.05em"}),
        ], style={
            "backgroundColor": "#1a1a1a",
            "color": "white",
            "padding": "15px 25px",
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "marginLeft": "-12px",
            "marginRight": "-12px",
        }),
        width=12
    ),
    className="mb-3"
    ),

    dbc.Row([
        dbc.Col([
            html.Label("Year"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": str(y), "value": y} for y in available_years],
                value=available_years[-1],
                clearable=False,
            ),
        ], width=3),
    ], className="mb-3"),

    # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/tabs/
    dbc.Tabs(id="tabs", active_tab="tab-neighborhood", children=[

        dbc.Tab(label="Neighborhood View", tab_id="tab-neighborhood", children=[

            dbc.Row([
                dbc.Col([
                    html.Label("Metric", className="mt-3"),
                    dcc.Dropdown(
                        id="metric-dropdown",
                        value="graduation_rate",
                        clearable=False,
                    ),
                ], width=4),
            ], className="my-2"),

            dbc.Row([
                # https://dash.plotly.com/dash-html-components/iframe
                # https://python-visualization.github.io/folium/latest/advanced_guide/flask.html
                dbc.Col(
                    html.Iframe(
                        id="base-map",
                        style={"width": "100%", "height": "600px", "border": "none"}
                    ),
                    width=7
                ),
                dbc.Col(
                    dcc.Graph(id="neighborhood-bar-chart", style={"height": "600px"}),
                    width=5
                ),
            ]),
        ]),

        dbc.Tab(label="School Comparison", tab_id="tab-comparison", children=[

            dbc.Row([
                dbc.Col([
                    html.Label("School A", className="mt-3"),
                    dcc.Dropdown(id="school-a-dropdown", clearable=False),
                ], width=4),
                dbc.Col([
                    html.Label("School B", className="mt-3"),
                    dcc.Dropdown(id="school-b-dropdown", clearable=False),
                ], width=4),
            ], className="my-2"),

            dbc.Row([
                dbc.Col(
                    html.Iframe(
                        id="comparison-map",
                        style={"width": "100%", "height": "600px", "border": "none"}
                    ),
                    width=7
                ),
                dbc.Col(
                    dcc.Graph(id="comparison-chart", style={"height": "600px"}),
                    width=5
                ),
            ]),
        ]),
    ]),

], fluid=True)


# Update metric dropdown options based on selected year
@callback(
    Output("metric-dropdown", "options"),
    Output("metric-dropdown", "value"),
    Input("year-dropdown", "value"),
)
def update_metric_options(year):
    schools = get_mappable_schools(school_data[school_data["year"] == year])
    available = get_available_metrics(schools, CHOROPLETH_METRICS)
    options = [{"label": m.replace("_", " ").title(), "value": m} for m in available]
    return options, available[0] if available else None


# Update neighborhood map when year or metric changes
@callback(
    Output("base-map", "srcDoc"),
    Input("year-dropdown", "value"),
)
def update_map(year):
    return make_base_map(year)._repr_html_()


# Update neighborhood bar chart when year or metric changes
@callback(
    Output("neighborhood-bar-chart", "figure"),
    Input("year-dropdown", "value"),
    Input("metric-dropdown", "value"),
)

def update_bar_chart(year, metric):
    schools = get_mappable_schools(school_data[school_data["year"] == year])
    agg = aggregate_by_neighborhood(schools, metric, year)
    agg = agg.sort_values(metric, ascending=True)

    # https://plotly.com/python/bar-charts/
    fig = px.bar(
        agg,
        x=metric,
        y="neighborhood",
        orientation="h",
        labels={
            metric: metric.replace("_", " ").title(),
            "neighborhood": ""
        },
        title=metric.replace("_", " ").title() + " by Neighborhood (" + str(int(year)) + ")",
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    return fig


# Populate school dropdowns when year changes
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


# Update comparison map when year changes
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
    comparison = get_school_comparison(schools, school_a, school_b)

    # https://plotly.com/python/grouped-bar-charts/ ## fix this link
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=school_a,
        x=comparison["metric"],
        y=comparison[school_a]
    ))
    fig.add_trace(go.Bar(
        name=school_b,
        x=comparison["metric"],
        y=comparison[school_b]
    ))

    fig.update_layout(
        barmode="group",
        title=school_a + " vs " + school_b + " (" + str(int(year)) + ")",
        xaxis_tickangle=-45,
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


if __name__ == "__main__":
    print("I AM RUNNING")
    app.run(debug=True)
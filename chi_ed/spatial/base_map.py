import folium
from .data import (
    load_neighborhoods,
    load_schools,
    get_mappable_schools,
    get_school_points,
    CLEAN_DATA_DIR,
)
from .aggregation import aggregate_by_neighborhood

neighborhoods = load_neighborhoods()
school_data = load_schools()


def make_base_map(
    year, metric=None, school_data=school_data, neighborhoods=neighborhoods
):
    """
    Making a neighborhood level map of Chicago with school locations
    layered on top

    Parameters:
        year: Year to filter school data by
        metric: Metric to be used in creating a choropleth map
        school_data: Data frame containing panel data of schools
        neighborhoods: Chicago neighborhood boundaries

    Returns:
        A choropleth neighborhood level map or standard map with school
        locations mapped on top
    """
    schools = get_mappable_schools(school_data[school_data["year"] == year]).copy()

    school_points = get_school_points(schools)

    display_cols = [
        "school_name",
        "graduation_rate",
        "sat_school_average",
        "college_enrollment_rate",
        "attendance_rate_current_year",
    ]

    # replace NaN and 0 with "N/A" for columns we are using for tooltip interaction
    # replace 0 SAT scores with N/A
    school_points["sat_school_average"] = school_points["sat_school_average"].replace(
        0, "N/A"
    )
    school_points[display_cols] = school_points[display_cols].fillna("N/A")

    # Focusing on center point of Chicago shapefiles
    center_lat = 41.85
    center_lon = -87.70

    # Documentation used: https://geopandas.org/en/stable/gallery/plotting_with_folium.html
    base_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles="CartoDB positron",
        width="100%",
        height="800px",
    )

    # Setting the dimensions to match iframe height
    base_map.get_root().width = "100%"
    base_map.get_root().height = "800px"

    # Creating a chloropleth map for the neighborhood tab in dash app
    if metric:
        # Aggregate metric by neighborhood for choropleth
        aggregated_metric = aggregate_by_neighborhood(schools, metric, year)

        # Adding choropleth layer colored for a given metric
        # Documentation: https://python-visualization.github.io/folium/latest/user_guide/geojson/choropleth.html
        folium.Choropleth(
            geo_data=neighborhoods,
            data=aggregated_metric,
            columns=["neighborhood", metric],
            key_on="feature.properties.pri_neigh",
            fill_color="Blues",
            fill_opacity=0.9,
            line_opacity=0.8,
            nan_fill_color="white",
            nan_fill_opacity=0.0,
            legend_name=metric.replace("_", " ").title(),
            name="Choropleth",
        ).add_to(base_map)

    # Adding chicago neighborhood level map on top of the base map
    folium.GeoJson(
        neighborhoods,
        name="Neighborhoods",
        # Documentation used for style of the map:
        # https://python-visualization.github.io/folium/latest/user_guide/geojson/geojson.html
        style_function=lambda feature: {
            "fillColor": "#d4e8f5" if not metric else "transparent",
            "fillOpacity": 0.4 if not metric else 0,
            "color": "#444444",
            "weight": 1.0,
        },
        zoom_on_click=True,
        tooltip=folium.GeoJsonTooltip(
            fields=["pri_neigh"],
            aliases=["Neighborhood:"],
            sticky=False,
            labels=True,
        ),
    ).add_to(base_map)

    # Overlaying schools on top of neighborhoods
    folium.GeoJson(
        school_points,
        name="Schools",
        marker=folium.Circle(
            radius=100,
            fill_color="#e85d26",
            fill_opacity=0.8,
            color="#e85d26",
            weight=1,
        ),
        tooltip=folium.GeoJsonTooltip(
            fields=display_cols,
            aliases=[
                "School:",
                "Graduation Rate:",
                "SAT Average:",
                "College Enrollment Rate:",
                "Attendance Rate:",
            ],
            sticky=False,
            labels=True,
        ),
    ).add_to(base_map)

    return base_map


if __name__ == "__main__":
    base_map = make_base_map(2025)
    base_map.save(str(CLEAN_DATA_DIR / "chicago_schools_map.html"))

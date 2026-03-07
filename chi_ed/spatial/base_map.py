import folium
import pandas as pd
import geopandas as gpd
import pathlib


SHAPEFILE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "chicago_neighborhoods"
SHAPEFILE_NAME = "geo_export_acac5c2b-cc20-4f75-b7fe-e0a1c11b1ab2.shp"
neighborhoods = gpd.read_file(SHAPEFILE_DIR / SHAPEFILE_NAME)

schools = pd.read_csv("/mnt/c/Users/mehwi/Downloads/merged_api_rc.csv")

# filter to most recent year
most_recent_year = schools["school_profile_year"].max()
schools = schools[schools["school_profile_year"] == most_recent_year]

# dropping schools with missing coordinates
schools = schools.dropna(subset=["address_latitude", "address_longitude"])

# fixing missing school names
schools["school_name"] = schools["school_name"].fillna(schools["school_long_name"])

# replace NaN and 0 with "N/A" for columns we are using for tooltip intercation
# replace 0 SAT scores with N/A
schools["sat_school_average"] = schools["sat_school_average"].replace(0, "N/A")

display_cols = [
    "school_name",
    "graduation_rate",
    "sat_school_average",
    "college_enrollment_rate",
    "attendance_rate_current_year"
]
schools[display_cols] = schools[display_cols].fillna("N/A")

school_points = gpd.GeoDataFrame(
    schools,
    geometry=gpd.points_from_xy(schools["address_longitude"], schools["address_latitude"]),
    crs="EPSG:4326"
)

# Creating a base map

# Focusing on center point of Chicago shapefiles
center_lat = 41.8781
center_lon = -87.6298

# Documentation used: https://geopandas.org/en/stable/gallery/plotting_with_folium.html
base_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles="CartoDB positron"
)

# Adding neighborhood level map on top of the base map
# Documentation used for style of the map: https://python-visualization.github.io/folium/latest/user_guide/geojson/geojson.html
folium.GeoJson(
    neighborhoods,
    name="Neighborhoods",
    style_function=lambda feature: {
        "fillColor": "transparent",
        "color": "#444444",
        "weight": 1.0,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["pri_neigh"],
        aliases=["Neighborhood:"]
    )
).add_to(base_map)

# Overlaying schools on top of neighborhoods
folium.GeoJson(
    school_points,
    name="Schools",
    marker=folium.Circle(
        radius=100,
        fill_color="steelblue",
        fill_opacity=0.8,
        color="steelblue",
        weight=1
    ),
    tooltip=folium.GeoJsonTooltip(
        fields=display_cols,
        aliases=[
            "School:",
            "Graduation Rate:",
            "SAT Average:",
            "College Enrollment Rate:",
            "Attendance Rate:"
        ],
        sticky=False,
        labels=True,
    )
).add_to(base_map)

# Saving the map as html
# base_map.save("/mnt/c/Users/mehwi/Downloads/chicago_schools_map.html")
output_path = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "clean"
base_map.save(output_path / "chicago_schools_map.html")
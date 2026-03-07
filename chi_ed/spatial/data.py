import geopandas as gpd
import pandas as pd
import pathlib

SHAPEFILE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "chicago_neighborhoods"
SHAPEFILE_NAME = "geo_export_acac5c2b-cc20-4f75-b7fe-e0a1c11b1ab2.shp"

# TODO: Add directory and file name etc for schools too

neighborhoods = gpd.read_file(SHAPEFILE_DIR/SHAPEFILE_NAME)
schools = pd.read_csv("/mnt/c/Users/mehwi/Downloads/merged_api_rc.csv")

school_points = gpd.GeoDataFrame(
    schools,
    geometry=gpd.points_from_xy(schools["address_longitude"], schools["address_latitude"]),
    crs="EPSG:4326"
)

spatial_join = gpd.sjoin(school_points, neighborhoods[["pri_neigh", "geometry"]], how="left", predicate="within")

schools_by_neighborhoods = {}
for neighborhood, df in spatial_join.groupby("pri_neigh"):
    schools_by_neighborhoods[neighborhood] = df["school_name"].tolist()

#output_path = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "schools_by_neighborhoods.json"
output_path = pathlib.Path("/mnt/c/Users/mehwi/Downloads/schools_by_neighborhoods.json")
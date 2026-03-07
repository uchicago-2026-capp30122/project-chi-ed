import geopandas as gpd
import pandas as pd
import pathlib

# SHAPEFILE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "chicago_neighborhoods"
# SHAPEFILE_NAME = "geo_export_acac5c2b-cc20-4f75-b7fe-e0a1c11b1ab2.shp"
# MERGED_DATA_DIR = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "outputs" / "merged_data"

# # TODO: Add directory and file name etc for schools too

# neighborhoods = gpd.read_file(SHAPEFILE_DIR/SHAPEFILE_NAME)

# #schools = pd.read_csv("/mnt/c/Users/mehwi/Downloads/merged_api_rc.csv")
# schools = pd.read_csv(MERGED_DATA_DIR/"merged_api_rc.csv")

# school_points = gpd.GeoDataFrame(
#     schools,
#     geometry=gpd.points_from_xy(schools["address_longitude"], schools["address_latitude"]),
#     crs="EPSG:4326"
# )

# spatial_join = gpd.sjoin(school_points, neighborhoods[["pri_neigh", "geometry"]], how="left", predicate="within")

# schools_by_neighborhoods = {}
# for _, row in spatial_join.iterrows():
#     schools_by_neighborhoods[row["school_name"]] = row["pri_neigh"]

# output_path = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "clean" / "schools_by_neighborhoods.json"


SHAPEFILE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "chicago_neighborhoods"
SHAPEFILE_NAME = "geo_export_acac5c2b-cc20-4f75-b7fe-e0a1c11b1ab2.shp"
MERGED_DATA_DIR = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "outputs" / "merged_data"
CLEAN_DATA_DIR = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "clean"

def load_neighborhoods():
    """
    Loads the Chicago neighborhoods shapefile.
    Returns a GeoDataFrame with neighborhood boundaries.
    """
    return gpd.read_file(SHAPEFILE_DIR / SHAPEFILE_NAME)

def load_schools(year=None):
    """
    Loads and cleans the merged CPS + ISBE school data.
    
    Parameters:
    - year: if provided, filters to that year. If None, uses most recent year.
    
    Returns a cleaned pandas DataFrame.
    """
    schools = pd.read_csv(MERGED_DATA_DIR / "merged_api_rc.csv")

    # Filtering by year
    if year is None:
        year = schools["school_profile_year"].max()
    schools = schools[schools["school_profile_year"] == year]

    # Dropping schools with missing address
    schools = schools.dropna(subset=["address_latitude", "address_longitude"])

    # fix missing school names
    schools["school_name"] = schools["school_name"].fillna(schools["school_long_name"])

    return schools


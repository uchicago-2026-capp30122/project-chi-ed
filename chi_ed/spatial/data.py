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

ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()
SHAPEFILE_DIR = ROOT / "data" / "chicago_neighborhoods"
SHAPEFILE_NAME = "geo_export_acac5c2b-cc20-4f75-b7fe-e0a1c11b1ab2.shp"
MERGED_DATA_DIR = ROOT / "data" / "outputs" / "merged_data"
CLEAN_DATA_DIR = ROOT / "data" / "clean"
CLEANED_DATA_FILE = "clean_panel.csv"

def load_neighborhoods():
    """
    Load Chicago neighborhood boundaries from shapefile.
    Key column is `pri_neigh`

    Returns:
        GeoDataFrame with neighborhood polygons in CRS EPSG:4326.     
    """
        
    return gpd.read_file(SHAPEFILE_DIR / SHAPEFILE_NAME)

# def load_schools(year=None):
#     
#     Loads and cleans the merged CPS + ISBE school data.
    
#     Parameters:
#     - year: if provided, filters to that year. If None, uses most recent year.
    
#     Returns a cleaned pandas DataFrame.
#     """
    
#     df = pd.read_csv(CLEAN_DATA_DIR / CLEANED_DATA_FILE)

#     # Impute missing year: if lat/lon present, it's 2025 API-only data
#     mask = df["year"].isna() & df["address_latitude"].notna() & df["address_longitude"].notna()
#     df.loc[mask, "year"] = 2025.0

#     # Drop rows with no coordinates (unusable for mapping)
#     df = df.dropna(subset=["address_latitude", "address_longitude"])

#     if year is not None:
#         df = df[df["year"] == year]

#     return df

def load_schools(year=None):
    """
    Loads the cleaned school panel data.

    Imputes missing year values for rows that came from the 2025 CPS API
    but had no matching ISBE report card entry. 

    Parameters:
        year: If provided, filters to only rows matching that school year.
    
    Returns:
        DataFrame with panel data for all schools, optionally filtered by year.
    """

    df = pd.read_csv(CLEAN_DATA_DIR / CLEANED_DATA_FILE)
    
    # Imputing missing year: if latitutde and longitude are present for a school, 
    # the data came in from API which only contains data from year 2025
    mask = df["year"].isna() & df["address_latitude"].notna() & df["address_longitude"].notna()
    df.loc[mask, "year"] = 2025.0
    
    if year is not None:
        df = df[df["year"] == year]
    
    return df

def get_mappable_schools(schools):
    """
    Filter schools to only those that can be plotted on a map.

    Parameters:
        schools: DataFrame output of load_schools.

    Returns:
        Subset of schools DataFrame with non-null latitude and longitude.
    """
    return schools.dropna(subset=["address_latitude", "address_longitude"])

def get_school_points(schools):
    """
    Convert a schools DataFrame to a GeoDataFrame of point geometries.

    Parameters:
        schools: DataFrame with `address_longitude` and `address_latitude` columns.

    Returns:
        GeoDataFrame with Point geometry in CRS EPSG:4326.
    """
    return gpd.GeoDataFrame(
        schools,
        geometry=gpd.points_from_xy(schools["address_longitude"], schools["address_latitude"]),
        crs="EPSG:4326"
    )


def get_spatial_join(school_points, neighborhoods):
    """
    Spatially join schools to neighborhoods based on point-in-polygon.

    Parameters:
        school_points: GeoDataFrame output of get_school_points.
        neighborhoods: GeoDataFrame output of load_neighborhoods.

    Returns:
        GeoDataFrame of schools with `pri_neigh` column added. 
        Schools outside any neighborhood polygon will have NaN for `pri_neigh`.
    """
    return gpd.sjoin(
        school_points,
        neighborhoods[["pri_neigh", "geometry"]],
        how="left",
        predicate="within"
    )



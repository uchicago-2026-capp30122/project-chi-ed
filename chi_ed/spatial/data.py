import geopandas as gpd
import pandas as pd
import pathlib

ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()
SHAPEFILE_DIR = ROOT / "data" / "shapefiles"
SHAPEFILE_NAME = "geo_export_acac5c2b-cc20-4f75-b7fe-e0a1c11b1ab2.shp"
MERGED_DATA_DIR = ROOT / "data" / "outputs" / "merged_data"
CLEAN_DATA_DIR = ROOT / "data" / "clean"
CLEANED_DATA_FILE = "clean_panel.csv"


def load_neighborhoods():
    """
    Loading Chicago neighborhood boundaries from shapefile.
    Key column is `pri_neigh`

    Returns:
        A geodataframe with neighborhood polygons in CRS EPSG:4326.
    """

    return gpd.read_file(SHAPEFILE_DIR / SHAPEFILE_NAME)


def load_schools(year=None):
    """
    Loads the cleaned school panel data.

    Imputing missing year if latitutde and longitude are present for a school,
    the data came in from API which only contains data from year 2025

    Parameters:
        year (optional): Year to filter school data by

    Returns:
        A data frame with panel data for all schools, optionally filtered by year
    """

    schools = pd.read_csv(CLEAN_DATA_DIR / CLEANED_DATA_FILE)

    mask = (
        schools["year"].isna()
        & schools["address_latitude"].notna()
        & schools["address_longitude"].notna()
    )
    schools.loc[mask, "year"] = 2025

    if year is not None:
        schools = schools[schools["year"] == year]

    schools = schools.replace("*", pd.NA)

    return schools


def get_mappable_schools(schools):
    """
    Filter school dataframe to keep only those that can be plotted on a map.

    Parameters:
        schools: Dataframe output of load_schools.

    Returns:
        A subset of schools with non-missing latitude and longitude.
    """
    return schools.dropna(subset=["address_latitude", "address_longitude"])


def get_school_points(schools):
    """
    Convert a schools dataframe to a geodataframe of point geometries.

    Parameters:
        schools: A data frame containing school information

    Returns:
        A geodataframe with point geometry in CRS EPSG:4326.
    """
    return gpd.GeoDataFrame(
        schools,
        geometry=gpd.points_from_xy(
            schools["address_longitude"], schools["address_latitude"]
        ),
        crs="EPSG:4326",
    )


def get_spatial_join(school_points, neighborhoods):
    """
    Spatially join schools to neighborhoods based on point-in-polygon.

    Parameters:
        school_points: A geodataframe of school locations with point geometry.
        neighborhoods: A geodataframe of Chicago neighborhood boundaries.

    Returns:
        A geodataframe of schools with `pri_neigh` column added.
    """

    return gpd.sjoin(
        school_points,
        neighborhoods[["pri_neigh", "geometry"]],
        how="left",
        predicate="within",
    )


def get_available_years():
    """
    Sorting the years present in the panel data.

    Returns:
        Sorted list of integers representing available school years.
    """
    df = pd.read_csv(CLEAN_DATA_DIR / CLEANED_DATA_FILE, usecols=["year"])
    return sorted(df["year"].dropna().unique().astype(int).tolist())

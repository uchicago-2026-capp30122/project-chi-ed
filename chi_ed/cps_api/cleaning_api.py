import polars as pl
from pathlib import Path
import re

# ------------------------------------------------------------------------------
# This code loads the raw api data that was fetched using the fetching_api_data
#   file, cleans the data, generatees some new columns of interest
# ------------------------------------------------------------------------------

RAW_DATA_API = Path(__file__).parent.parent.parent / "data/raw/api_data/api_data.json"
CSV_PATH = Path(__file__).parent.parent.parent / "data/outputs/api_data/api_data.csv"
API_DATA_COLS = [
    # Location / Transit
    "AddressLongitude",
    "AddressLatitude",
    "SchoolShortName",
    "SchoolLongName",
    "AddressStreet",
    "AddressZipCode",
    "HasTransitionProgram",
    "TransportationBus",
    "TransportationEL",
    "TransportationMetra",
    # Outcomes of interest
    "GraduationRate",
    "SATSchoolAverage",
    "DistrictMeanGraduationRate",
    "GraduationRate4Year",
    "DistrictMeanCollegeEnrollmentRate",
    "CollegeEnrollmentRate",
    "AttendanceRateCurrentYear",
    # School composition/diversity
    "StudentCount",
    "StudentCountLowIncome",
    "StudentCountSpecialEducation",
    "StudentCountBlack",
    "StudentCountHispanic",
    "StudentCountWhite",
    "StudentCountAsian",
    "StudentCountNativeAmerican",
    "StatisticsSummary",
    "DemographicsSummary",
    # Other facilities/indicators
    "HasBilingualServices",
    "HasRefugeeServices",
    "HasHearingImpairmentServices",
    "HasVisualImpairmentServices",
    "SchoolProfileYear",
    "SafetyRating",
    "CultureRating",
    "SchoolYearReadable",
    "OverallRatingStatus",
    "OverallRating",
]


def clean_api_json(filename: Path = RAW_DATA_API):
    """
    This function loads the JSON API data as a polars dataframe, performs basic
    cleaning on it and selects only the relevant columns for our analysis and 
    returns the cleaned dataframe.

    Inputs:
        filename: Path object for the raw API JSON data file

    Returns: 
        dataframe: returns the cleaned API data as polars dataframe
    """
    api_df = pl.read_json(filename, infer_schema_length=200)
    api_df = api_df.filter(
        pl.col("IsHighSchool") == True
    )  # Should yield 173 highschools
    api_df = api_df.select(API_DATA_COLS)  # .select(pl.all().name.to_lowercase())

    api_df = api_df.with_columns(
        pl.col("AddressZipCode").str.split(by="-").list.get(0).alias("zip"),
        # Generating numeric columns to count the number of buses and trains connecting the school
        (
            pl.col("TransportationEL").str.count_matches(",")
            + pl.when(pl.col.TransportationEL.str.len_chars() > 0).then(1).otherwise(0)
        ).alias("el_connections"),
        (
            pl.col("TransportationBus").str.count_matches(",")
            + pl.when(pl.col.TransportationEL.str.len_chars() > 0).then(1).otherwise(0)
        ).alias("cta_connections"),
        (
            pl.col("TransportationMetra").str.count_matches(",")
            + pl.when(pl.col.TransportationEL.str.len_chars() > 0).then(1).otherwise(0)
        ).alias("metra_connections"),
    )

    api_df = api_df.drop("AddressZipCode")
    # Cleaning column names
    api_df = api_df.rename(
        lambda column_name: re.sub(r"(?<!^)(?=[A-Z][a-z])", "_", column_name).lower()
    )
    # re source: https://stackoverflow.com/questions/75294852/string-manipulation-in-polars

    return api_df


def write_csv(input_filename: Path = RAW_DATA_API, output_filename: Path = CSV_PATH):
    """
    This function takes in the raw API filepaths and writes the csv data on the 
    specified output filepath.

    Inputs:
        input_filename: Path object for the raw API JSON data file
        output_filename: Path object for the filename we want to write the csv on
    """
    api_data = clean_api_json(input_filename)
    api_data.write_csv(output_filename)


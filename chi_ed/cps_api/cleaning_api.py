import polars as pl
from pathlib import Path
import re

# This file loads the raw api data that was downloaded and saves a clean csv
#   file with selected variables of interest

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


def clean_json(filename: Path = RAW_DATA_API):
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
    api_data = clean_json(input_filename)
    api_data.write_csv(output_filename)


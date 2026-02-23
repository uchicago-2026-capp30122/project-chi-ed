import polars as pl
from pathlib import Path
import csv
import json

# This file loads the raw api data that was downloaded and saves a clean csv 
#   file with selected variables of interest

RAW_DATA_API = Path(__file__).parent.parent.parent / "data/raw/api_data/api_data.json"
CSV_PATH = Path(__file__).parent.parent.parent / "data/outputs/api_data/api.csv"
API_DATA_COLS = ["SATSchoolAverage", "AddressLongitude", "AddressLatitude", "SchoolShortName", "SchoolLongName", "AddressZipCode"]

def load_json(filename: Path = RAW_DATA_API):
    with open(filename, "r") as json_data:
        api_data = json.load(json_data)
    return api_data

def clean_json(filename: Path = RAW_DATA_API):
    api_data = pl.read_json(load_json(filename), infer_schema_length=200)
    api_data = api_data.filter(pl.col("IsHighSchool") == True) # should yield 173 highschools
    api_data = api_data.select(API_DATA_COLS).select(pl.all().name.to_lowercase())

    # cleaning the zip code
    api_data = api_data.with_columns(
        pl.col("addresszipcode")
        .str.split(by="-")
        .list.get(0).alias("zip")
    )

    api_data = api_data.drop("addresszipcode")
    return api_data

    # pending cleaning work:
        # - Convert cols to snake case
        # - add more vars
        # - do comprehensive string cleaning
        # - add docstrings for functions

def write_csv(input_filename: Path=RAW_DATA_API, output_filename: Path=CSV_PATH):
    api_data = clean_json(input_filename)
    api_data.write_csv(output_filename)












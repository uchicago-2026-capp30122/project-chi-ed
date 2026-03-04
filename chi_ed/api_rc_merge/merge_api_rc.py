from merge_rc_dir import merge_for_zip, REPORT_CARD_PATH, DIRECTORY_DATA_PATH
from cps_api.cleaning_api import clean_api_json, RAW_DATA_API
import jellyfish
import polars as pl
import re
from pathlib import Path

# ------------------------------------------------------------------------------
# In this code we use fuzzy matching to link & merge API data with report card data
# ------------------------------------------------------------------------------

MERGE_CSV_PATH = (
    Path(__file__).parent.parent.parent / "data/outputs/maerged_data/merged_api_rc.csv"
)


def merge_api_rc(output_filname: Path = MERGE_CSV_PATH):
    """
    This function takes in a Path object and inside the function we are importing
    different data sources, performing a fuzzy match and writing the merged data
    as a csv file.

    Inputs:
        output_filename: Path object for where we write the csv merged data
    """
    report_card_df = merge_for_zip(DIRECTORY_DATA_PATH, REPORT_CARD_PATH)
    api_df = clean_api_json(RAW_DATA_API)

    api_df = api_df.rename({"school_long_name"})

    api_school_zip = pl.Series(
        api_df.select(pl.concat_list("school_short_name", "zip"))
    ).to_list()
    rc_school_zip = pl.Series(
        report_card_df.select(pl.concat_list("school_name", "zip"))
    ).to_list()

    # Converting list of list to dict for faster lookups

    api_dict = {key: value for key, value in api_school_zip}
    rc_dict = {key: value for key, value in rc_school_zip}

    school_similarity_lookup = dict()

    for school_x, zip_x in api_dict.items():
        school_similarity_lookup[school_x] = []
        same_zip_schools = {}
        same_zip_schools[school_x] = []
        for school_y, zip_y in rc_dict.items():
            if zip_y == zip_x:
                same_zip_schools[school_x].append(school_y)
        for matched_school in same_zip_schools[school_x]:
            clean_school_x = (
                school_x.lower().
                replace("high school", "")
                .replace("hs", "")
                .strip()
            )
            clean_matched_school = (
                matched_school.lower()
                .replace("high school", "")
                .replace("hs", "")
                .strip()
            )
            if (
                jellyfish.jaro_winkler_similarity(clean_school_x, clean_matched_school)
                > 0.71 # Only one school is being wrongly matched 
            ):
                school_similarity_lookup[school_x].append(
                    (
                        matched_school,
                        jellyfish.jaro_winkler_similarity(
                            clean_school_x, clean_matched_school
                        ),
                    )
                )

    matched = 0

    for _, v in school_similarity_lookup.items():
        v = sorted(v, key=lambda tup: tup[1], reverse=True)
        if v:
            matched += 1
            v = v[0]

    
from chi_ed.merging.merge_rc_dir import (
    merge_for_zip,
    REPORT_CARD_PATH,
    DIRECTORY_DATA_PATH,
)
from chi_ed.cps_api.cleaning_api import clean_api_json, RAW_DATA_API
import jellyfish
import polars as pl
import re
from pathlib import Path
from collections import defaultdict

# ------------------------------------------------------------------------------
# In this code we use fuzzy matching to link & merge API data with report card data
# ------------------------------------------------------------------------------

MERGE_CSV_PATH = (
    Path(__file__).parent.parent.parent / "data/outputs/merged_data/merged_api_rc.csv"
)


def matched_schools(api_dict: dict, rc_dict: dict) -> dict:
    """
    This funcion takes in two dictionaries built from our two data sources,
    containing key, value pairs for school names and their zip codes and builds
    a lookup dictionary where we match each school from the API data to a school
    from the report card data based on Jaro Winkler Similarity score.

    The threshold here has been set to 0.71 which was validated through manual
    inspection of all the matches. Only one school was wrongly matched which
    is handled explicitly.

    This code successfully matches 134 out of 141 schools in the report card data,
    there are 32 additional schools only in the API data.

    Inputs:
        api_dict: Dictionary containing key value pairs for school names and zips
                    for the API data
        rc_dict: Dictionary containing key value pairs for school names and zips
                    for the report card data

    Returns:
        Dictionary containing key value pairs for matching schools based on the
        highest Jaro Winkler Similarity score
    """
    school_similarity_lookup = dict()

    for school_api, zip_api in api_dict.items():
        school_similarity_lookup[
            school_api
        ] = []  # Not using default dict here to keep track of schools with no matches
        same_zip_schools = defaultdict(list)

        for school_rc, zip_rc in rc_dict.items():
            if zip_rc == zip_api:
                same_zip_schools[school_api].append(school_rc)

        for matched_school in same_zip_schools[school_api]:
            # Cleaning school names ahead of comparisons
            clean_school_api = school_api.lower().replace("hs", "").strip()
            clean_matched_school = (
                matched_school.lower()
                .replace("high school", "")
                .replace("hs", "")
                .strip()
            )
            if (
                jellyfish.jaro_winkler_similarity(
                    clean_school_api, clean_matched_school
                )
                > 0.71  # Only one school is being wrongly matched using this threshold
            ):
                school_similarity_lookup[school_api].append(
                    (
                        matched_school,
                        jellyfish.jaro_winkler_similarity(
                            clean_school_api, clean_matched_school
                        ),
                    )
                )

    school_similarity_lookup[
        "EXCEL ENGLEWOOD HS"
    ] = []  # this school was wrongly matched

    for k, v in school_similarity_lookup.items():
        v = sorted(v, key=lambda tup: tup[1], reverse=True)
        if v:
            v = v[0]
            school_similarity_lookup.update({k: v[0]})
        else:
            school_similarity_lookup.update({k: ""})

    return school_similarity_lookup


def merge_api_rc() -> pl.DataFrame:
    """
    This function takes in a Path object, and returns a merged dataframe with
    all the schools in the API data merged with the schools in the report card 
    data. We perform a full merge to keep the schools that are in one 21    /lqa

    Returns:
        Merged Dataframe containing data from both API and Report card data
    """
    report_card_df = merge_for_zip(
        DIRECTORY_DATA_PATH, REPORT_CARD_PATH
    )  # Merging report card data with direcotry data to get zip codes
    api_df = clean_api_json(RAW_DATA_API)

    api_school_zip = pl.Series(
        api_df.select(pl.concat_list("school_short_name", "zip"))
    ).to_list()
    rc_school_zip = pl.Series(
        report_card_df.select(pl.concat_list("school_name", "zip"))
    ).to_list()

    # Converting list of list to dict for faster lookups
    api_dict = {key: value for key, value in api_school_zip}
    rc_dict = {key: value for key, value in rc_school_zip}

    school_lookup = matched_schools(api_dict, rc_dict)

    # Converting lookup dict to df for merging
    mapper = pl.DataFrame(
        {
            "school_short_name": list(school_lookup.keys()),
            "school_name": list(school_lookup.values()),
        }
    )

    api_df = api_df.join(
        mapper, on="school_short_name", how="inner"
    )  # We do an inner join here because there should be a 1:1 correspondence

    merged_df = report_card_df.join(
        api_df, on="school_name", how="full"
    )  # We do a full join here to keep the schools that were not matched across both datasets

    return merged_df


def write_merged_data(output_filname: Path = MERGE_CSV_PATH):
    """
    This function gets the merged dataframe using the merge_api_rc function and
    writes the dataframe as a csv on the path given as input

    Inputs:
        output_filename: Path object where the csv file will be written
    """
    merged_df = merge_api_rc()
    merged_df.write_csv(output_filname)

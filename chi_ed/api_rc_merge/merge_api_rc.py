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

    for school_x, zip_x in api_dict.items():
        school_similarity_lookup[school_x] = []
        same_zip_schools = {}

        same_zip_schools[school_x] = []
        for school_y, zip_y in rc_dict.items():
            if zip_y == zip_x:
                same_zip_schools[school_x].append(school_y)

        for matched_school in same_zip_schools[school_x]:
            clean_school_x = (
                school_x.lower().replace("hs", "").strip()
            )
            clean_matched_school = (
                matched_school.lower()
                .replace("high school", "")
                .replace("hs", "")
                .strip()
            )
            if (
                jellyfish.jaro_winkler_similarity(clean_school_x, clean_matched_school)
                > 0.71  # Only one school is being wrongly matched
            ):
                school_similarity_lookup[school_x].append(
                    (
                        matched_school,
                        jellyfish.jaro_winkler_similarity(
                            clean_school_x, clean_matched_school
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

    api_df = api_df.join(mapper, on="school_short_name", how="inner")

    merged_df = report_card_df.join(api_df, on="school_name", how="full")

    merged_df.write_csv(output_filname)

"""Helper functions to HTTP request or load data, or merge data"""

import pathlib
import pandas
import json
from ..schools import data
from ..schools.data import Schools, COLUMNS_2025_REPORTS_CARDS

COLNAMES_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "raw" / "colnames"


def load_reports_card(filepath):
    if not filepath.exists():
        raise ValueError(f"File path does not exist: {filepath}")

    # Load all necessary sheets from the Excel file
    # NOTE: This is particular to the 2025 report cards and will need modification if we add more years
    # Also call Schools.data to get the dataframe object
    general_dt = Schools(pandas.read_excel(filepath, sheet_name = "General"))
    scores_dt = Schools(pandas.read_excel(filepath, sheet_name = "ELAMathScience"))
    scores2_dt = Schools(pandas.read_excel(filepath, sheet_name = "ELAMathScience (2)"))
    finance_dt = Schools(pandas.read_excel(filepath, sheet_name = "Finance"))

    # Select + rename columns of interest
    columns_to_keep = [col for key in COLUMNS_2025_REPORTS_CARDS.keys() for col in COLUMNS_2025_REPORTS_CARDS[key].keys()]
    columns_mapping = {col: COLUMNS_2025_REPORTS_CARDS[key][col] for key in COLUMNS_2025_REPORTS_CARDS.keys() for col in COLUMNS_2025_REPORTS_CARDS[key].keys()}
    
    # NOTE: using contains = False because we are using a unique columns dict across all datasets
    general_dt.select_columns(columns_to_keep, contains = False)
    general_dt.rename_columns(columns_mapping)

    scores_dt.select_columns(columns_to_keep, contains = False)
    scores_dt.rename_columns(columns_mapping)

    scores2_dt.select_columns(columns_to_keep, contains = False)
    scores2_dt.rename_columns(columns_mapping)

    finance_dt.select_columns(columns_to_keep, contains = False)
    finance_dt.rename_columns(columns_mapping)

    # Common columns across all sheets
    common_colnames = ['RCDTS', 'school_name', 'school_type', 'county', 'city', 'district']

    # Merge all sheets on the common columns and now maintain the pandas.DataFrame objects
    merged_df = pandas.merge(general_dt.data, scores_dt.data, on = common_colnames, how = 'left')
    merged_df = pandas.merge(merged_df, scores2_dt.data, on = common_colnames, how = 'left')
    merged_df = pandas.merge(merged_df, finance_dt.data, on = common_colnames, how = 'left')

    # Filter to "Hight Schools" only
    merged_df = merged_df[merged_df['school_type'].str.strip() == 'High School']

    # Filter to "Chicago" 
    merged_df = merged_df[merged_df['city'].str.strip() == 'Chicago']

    return Schools(merged_df)



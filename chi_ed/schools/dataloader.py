"""Helper functions to HTTP request or load data, or merge data"""

import pathlib
import pandas
import json
from ..schools import data
from ..schools.data import Schools, COLUMNS_2025_REPORTS_CARDS

COLNAMES_DIRPATH = (
    pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "raw" / "colnames"
)


def _find_sheet(excel_file: pandas.ExcelFile, candidates: list[str]) -> str | None:
    """Return the first sheet name from candidates that exists in the Excel file, or None.
    I want to be very flexible to accommodate for different sheet names across years"""
    available = excel_file.sheet_names

    for sheet_name in candidates:
        if sheet_name in available:
            return sheet_name
    return None


def load_reports_card(filepath: pathlib.Path):
    if not filepath.exists():
        raise ValueError(f"File path does not exist: {filepath}")

    # Load the excel file
    excel_file = pandas.ExcelFile(filepath)

    # Try to find correct sheet names
    # NOTE: These are the sheet names across years (2019-2025)
    general_sheet = _find_sheet(excel_file, ["General"])
    scores_sheet = _find_sheet(
        excel_file, ["ELAMathScience", "ELA Math Science", "ELA and Math"]
    )
    scores2_sheet = _find_sheet(excel_file, ["ELAMathScience (2)"])

    # Strict error handling for general sheet which contains metadata
    if general_sheet is None:
        raise ValueError(f"No 'General' sheet found in {filepath}")

    # Load the general sheet
    general_dt = Schools(pandas.read_excel(excel_file, sheet_name=general_sheet))

    # Load the other sheets (only if they exist)
    other_sheets = []
    if scores_sheet:
        other_sheets.append(
            Schools(pandas.read_excel(excel_file, sheet_name=scores_sheet))
        )
    if scores2_sheet:
        other_sheets.append(
            Schools(pandas.read_excel(excel_file, sheet_name=scores2_sheet))
        )

    # Select + rename columns of interest
    columns_to_keep = [
        col
        for key in COLUMNS_2025_REPORTS_CARDS.keys()
        for col in COLUMNS_2025_REPORTS_CARDS[key].keys()
    ]
    columns_mapping = {
        col: COLUMNS_2025_REPORTS_CARDS[key][col]
        for key in COLUMNS_2025_REPORTS_CARDS.keys()
        for col in COLUMNS_2025_REPORTS_CARDS[key].keys()
    }

    list_of_sheets = [general_dt] + other_sheets
    # NOTE: using contains = False because we are using a unique columns dict across all datasets
    for sheet_data in list_of_sheets:
        sheet_data.select_columns(columns_to_keep, contains=False)
        sheet_data.rename_columns(columns_mapping)

    # Common columns across all sheets
    common_colnames = [
        "RCDTS",
        "school_name",
        "school_type",
        "county",
        "city",
        "district",
    ]

    # Merge all sheets on the common columns
    merged_df = general_dt.data
    for sheet_dt in other_sheets:
        merged_df = pandas.merge(
            merged_df, sheet_dt.data, on=common_colnames, how="left"
        )

    # Filter to "High Schools" only
    merged_df = merged_df[
        merged_df["school_type"].str.strip().str.lower() == "high school"
    ]

    # Filter to "Chicago" (case-insensitive for safety)
    merged_df = merged_df[merged_df["city"].str.strip().str.lower() == "chicago"]

    return Schools(merged_df)

"""Main script to clean the school data"""

import pathlib
import pandas
import csv
import json
from .data import Schools, COLUMNS_2025_REPORTS_CARDS
from .dataloader import load_reports_card


DATA_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" 
OUTPUTS_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "outputs" 

def import_data(filepath: pathlib.Path = None, raw: bool = True):
    """Import raw or cleaned version of the data. 
    N0TE: For raw data this function is designed for report carrds"""
    if raw:
        data = load_reports_card(DATA_DIRPATH / "raw" / "report_card_data" / "2025 ISBE Reports Card.xlsx")
    else:
        if not filepath.exists():
            raise ValueError(f"File path does not exist: {filepath}")
        data = Schools(pandas.read_csv(filepath))

    return data


def clean_reports_data():
    """Clean report cards and merge with API data"""
    # TODO: Complete this function to export merged and cleaned data for reports 
    # (1) Clean the 2025 ISBE Reports Card data if it is not already cleaned
    # NOTE: Export the cleaned version if first importing this data locally
    cards_2025_dt = import_data(filepath = DATA_DIRPATH / "clean" / "report_cards_2025.csv", raw = False)

    # (2) Import the merged report cards and API data 
    # NOTE: I iwll use import_data() even though that function seems designed for report card data. It is flexible on non-raw data
    merged_dt = import_data(filepath = DATA_DIRPATH / "outputs" / "merged_data" / "merged_api_rc.csv", raw = False)

    # Save all columns names
    with open(OUTPUTS_DIRPATH / "explore" / "columns_merged_api_rc.txt", "w") as f:
        for col in merged_dt.columns:
            f.write(col + "\n")


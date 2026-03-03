from pathlib import Path
import polars as pl
import re

REPORT_CARD_PATH = Path(__file__).parent.parent.parent / "data/outputs/report_cards_2025.csv"
DIRECTORY_DATA_PATH = Path(__file__).parent.parent.parent / "data/raw/aux_data/dir_ed_entities.xls"

# ------------------------------------------------------------------------------
# This code merges the report card csv dataset with school directory data to get zip codes
# ------------------------------------------------------------------------------

def merge_for_zip(directory_data: Path = DIRECTORY_DATA_PATH, report_card_data: Path = REPORT_CARD_PATH):
    """
    This function reads in chicago public schools directory data and Illinois
    schools report card data, and merges the two datasets on RCDTS to add the 
    zip code that is missing from the report card data

    Inputs:
        directory_data_filepath: filepath for directory data
        report_card_data: filepath for report card data

    Return:
        Returns polars dataframe for the merged data
    """

    report_card = pl.read_csv(report_card_data)
    dir_ed = pl.read_excel(directory_data, sheet_name="1 Public Dist & Sch")

    dir_ed = dir_ed.rename({"Region-2\nCounty-3\nDistrict-4": "RCD"})

    # Cleaning the RCDTS variable before merging

    dir_ed = dir_ed.with_columns(
        (pl.col("RCD") + pl.col("Type") + pl.col("School")).alias("RCDTS"),
        (pl.col("Zip").str.slice(0, 5).alias("zip"))
    )

    dir_ed = dir_ed.select(pl.col("RCDTS"), pl.col("zip"))

    report_card = report_card.with_columns(
        pl.col("RCDTS").str.replace_all(r"\-", "")
    )

    merged_df = report_card.join(
        dir_ed,
        on="RCDTS",
        how="inner"
    )

    return merged_df



"""Helper functions to HTTP request or load data, or merge data"""

import pathlib
import pandas
import json

COLNAMES_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "raw" / "colnames"


def select_columns(df, colnames, colnames_pairs):
    # Select columns
    df = df[df.columns[df.columns.isin(colnames)]]

    # Rename each column
    # NOTE: I feel like this is really inefficient!!! 
    # TODO: I might be able to combine this step with the above step (selection)
    for col in df.columns:
        for pair in colnames_pairs:
            if col == pair[0]:
                df.rename(columns = {col: pair[1]}, inplace = True)   
                break

    return df


def load_reports_card(filepath, year):
    # NOTE: The year argument is used to load the dictionary of columns of interest
    if not filepath.exists():
        raise ValueError(f"File path does not exist: {filepath}")

    # Load all necessary sheets from the Excel file
    general_df = pandas.read_excel(filepath, sheet_name = "General")
    scores_df = pandas.read_excel(filepath, sheet_name = "ELAMathScience")
    scores2_df = pandas.read_excel(filepath, sheet_name = "ELAMathScience (2)")
    finance_df = pandas.read_excel(filepath, sheet_name = "Finance")

    # Import dictionary of columns we are interested in
    valid_colnames_pairs = []
    with open(COLNAMES_DIRPATH / f"{year}_reports_cards.json", "r") as colnames_file:
        colnames_df = json.load(colnames_file)

        # Add the pairs (current column name, new column name)
        for col_type in colnames_df.keys():
            for col, name in colnames_df[col_type].items():
                valid_colnames_pairs.append((col, name))
    
    # Select + renames columns of interest
    valid_colnames = [pair[0] for pair in valid_colnames_pairs]
    general_df = select_columns(general_df, valid_colnames, valid_colnames_pairs)
    scores_df = select_columns(scores_df, valid_colnames, valid_colnames_pairs)
    scores2_df = select_columns(scores2_df, valid_colnames, valid_colnames_pairs)
    finance_df = select_columns(finance_df, valid_colnames, valid_colnames_pairs)

    # Find intersection of columns across all sheets
    common_colnames = ['RCDTS', 'school_name', 'school_type', 'county', 'city', 'district']

    # Merge all sheets on the common columns
    merged_df = pandas.merge(general_df, scores_df, on = common_colnames, how='left')
    merged_df = pandas.merge(merged_df, scores2_df, on = common_colnames, how='left')
    merged_df = pandas.merge(merged_df, finance_df, on = common_colnames, how='left')

    # Filter to "Hight Schools" only
    merged_df = merged_df[merged_df['school_type'].str.strip() == 'High School']

    # Filter to "Chicago" 
    merged_df = merged_df[merged_df['city'].str.strip() == 'Chicago']

    return merged_df

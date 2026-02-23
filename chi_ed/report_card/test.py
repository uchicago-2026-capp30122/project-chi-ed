import pathlib
import pandas
import csv


DATA_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" 

def load_reports_card(year):
    # Create the file path
    fpath = DATA_DIRPATH / "raw" / f"{year} ISBE Reports Card.xlsx"

    if not fpath.exists():
        raise ValueError(f"File path does not exist: {fpath}")
    
    general_df = pandas.read_excel(fpath, sheet_name="General")
    scores_df = pandas.read_excel(fpath, sheet_name="ELAMathScience")
    scores2_df = pandas.read_excel(fpath, sheet_name="ELAMathScience (2)")
    finance_df = pandas.read_excel(fpath, sheet_name="Finance")

    # Save column names in .txt files
    with open(DATA_DIRPATH / "outputs" / "reports_2025_general_colnames.txt", 'w') as txt_file:
        for col in general_df.columns:
            txt_file.write(col)
            txt_file.write("\n")

    with open(DATA_DIRPATH / "outputs" / "reports_2025_scores_colnames.txt", 'w') as txt_file:
            for col in scores_df.columns:
                txt_file.write(col)
                txt_file.write("\n")

    with open(DATA_DIRPATH / "outputs" / "reports_2025_scores2_colnames.txt", 'w') as txt_file:
            for col in scores2_df.columns:
                txt_file.write(col)
                txt_file.write("\n")

    with open(DATA_DIRPATH / "outputs" / "reports_2025_finance_colnames.txt", 'w') as txt_file:
            for col in finance_df.columns:
                txt_file.write(col)
                txt_file.write("\n")
            


load_reports_card(year = 2025)
import pathlib
import pandas
import csv
import json
from . import dataloader
from ..schools import data
from ..schools.data import Schools
from ..viz import mapping_utils, pdfs_utils


DATA_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" 
CARDS_2025_DIRPATH = DATA_DIRPATH / "raw" / "report_card_data" / "2025 ISBE Reports Card.xlsx"
CLEAN_CARDS_2025_DIRPATH = DATA_DIRPATH / "clean" / "report_cards_2025.csv"

OUTPUTS_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "outputs" 

def import_data(raw = False):
    """Writing this function to avoid having to import the raw data at each execution.
    It is a costly execution, so I want to minimize repeating it."""
    if raw:
        data = dataloader.load_reports_card(CARDS_2025_DIRPATH, 2025)
    else:
        data = pandas.read_csv(CLEAN_CARDS_2025_DIRPATH)

    return Schools(data)


if CLEAN_CARDS_2025_DIRPATH.exists():
    cards_2025 = import_data(raw = False)
else:
    cards_2025 = import_data(raw = True)
cards_2025.save_csv(CLEAN_CARDS_2025_DIRPATH)


cards_2025_df = cards_2025.select_columns(["teacher_attendance_rate", "math_proficiency"]) # "chronic_absenteeism", "ELA_proficiency",

bar_plot1 = mapping_utils.plot_bar_graph(cards_2025_df, "math_proficiency", 
                        school1 = "Intrinsic 2 Charter High School", 
                        school2 = "Steinmetz College Prep HS"
                    )

bar_plot2 = mapping_utils.plot_bar_graph(cards_2025_df, "teacher_attendance_rate", 
                        school1 = "Intrinsic 2 Charter High School", 
                        school2 = "Steinmetz College Prep HS"
                    )




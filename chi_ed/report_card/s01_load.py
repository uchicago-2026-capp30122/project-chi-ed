import pathlib
import pandas
import csv
import json
import dataloader
from ..schools import data 
from data import Schools


DATA_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" 


# Load 2025 reports card data 
cards_2025_filepath = DATA_DIRPATH / "raw" / "2025 ISBE Reports Card.xlsx"


cards_2025_df = dataloader.load_reports_card(cards_2025_filepath, 2025)


print(cards_2025_df)













# cards_2025_df.to_csv(DATA_DIRPATH / "outputs" / "report_cards_2025.csv", index = False)

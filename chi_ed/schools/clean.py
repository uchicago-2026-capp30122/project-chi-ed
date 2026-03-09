"""Main script to clean the school data"""

import pathlib
import pandas
import csv
import json
from .data import Schools
from .dataloader import load_reports_card


DATA_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "data"
OUTPUTS_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "outputs"


def import_data(filepath: pathlib.Path = None, raw: bool = True, year: int = None):
    """Import raw or cleaned version of the data.
    N0TE: For raw data this function is designed for report carrds"""
    if raw:
        data = load_reports_card(filepath)
        # Set the year column
        data.set_year_attribute(year)
    else:
        if not filepath.exists():
            raise ValueError(f"File path does not exist: {filepath}")
        data = Schools(pandas.read_csv(filepath))

    return data


def clean_reports_data():
    """Clean report cards and create panel data from 2019 to 2025"""
    # NOTE: This function is costly. Call it only if necessary.
    cards_2025_dt = import_data(
        filepath=DATA_DIRPATH
        / "raw"
        / "report_card_data"
        / "2025 ISBE Reports Card.xlsx",
        raw=True,
        year=2025,
    )
    cards_2024_dt = import_data(
        filepath=DATA_DIRPATH
        / "raw"
        / "report_card_data"
        / "2024 ISBE Reports Card.xlsx",
        raw=True,
        year=2024,
    )
    cards_2023_dt = import_data(
        filepath=DATA_DIRPATH
        / "raw"
        / "report_card_data"
        / "2023 ISBE Reports Card.xlsx",
        raw=True,
        year=2023,
    )
    cards_2022_dt = import_data(
        filepath=DATA_DIRPATH
        / "raw"
        / "report_card_data"
        / "2022 ISBE Reports Card.xlsx",
        raw=True,
        year=2022,
    )
    cards_2021_dt = import_data(
        filepath=DATA_DIRPATH
        / "raw"
        / "report_card_data"
        / "2021 ISBE Reports Card.xlsx",
        raw=True,
        year=2021,
    )
    cards_2020_dt = import_data(
        filepath=DATA_DIRPATH
        / "raw"
        / "report_card_data"
        / "2020 ISBE Reports Card.xlsx",
        raw=True,
        year=2020,
    )
    cards_2019_dt = import_data(
        filepath=DATA_DIRPATH
        / "raw"
        / "report_card_data"
        / "2019 ISBE Reports Card.xlsx",
        raw=True,
        year=2019,
    )

    # Save each data for preview
    list_of_data = [
        cards_2025_dt,
        cards_2024_dt,
        cards_2023_dt,
        cards_2022_dt,
        cards_2021_dt,
        cards_2020_dt,
        cards_2019_dt,
    ]
    for data in list_of_data:
        data.save_csv(DATA_DIRPATH / "clean" / f"{data.year}_report_cards.csv")

    # Create panel data but flexible on columns
    panel_data_df = pandas.concat(
        [
            cards_2025_dt.data,
            cards_2024_dt.data,
            cards_2023_dt.data,
            cards_2022_dt.data,
            cards_2021_dt.data,
            cards_2020_dt.data,
            cards_2019_dt.data,
        ],
        ignore_index=True,
    )

    # Sort by school name and year
    # NOTE: This is a unique method to report cards
    panel_data_df = panel_data_df.sort_values(by=["RCDTS", "year"]).reset_index(
        drop=True
    )
    panel_data = Schools(panel_data_df)

    # Correct school names so that each RCDTS has a unique school name
    panel_data.correct_school_names()

    # Save the panel data
    panel_data.save_csv(DATA_DIRPATH / "clean" / "panel_report_cards.csv")

    print(
        f"Panel data has: \n{panel_data.data['RCDTS'].nunique()} schools \n{panel_data.data['year'].nunique()} years"
    )

    return panel_data


def clean_merged_data(version: str):
    """Clean the merged data"""
    if version in ["raw", "intermediate"]:
        if version == "raw":
            panel_dt = clean_reports_data()
            return

        elif version == "intermediate":
            panel_dt = import_data(
                filepath=DATA_DIRPATH / "clean" / "panel_report_cards.csv", raw=False
            )

        merged_dt = import_data(
            filepath=DATA_DIRPATH / "clean" / "merged_panel_api_2025.csv", raw=False
        )

        columns_ISBE = set(panel_dt.data.columns)
        columns_API = set(merged_dt.data.columns) - columns_ISBE

        columns_dict = {"ISBE": list(columns_ISBE), "API": list(columns_API)}

        with open(
            DATA_DIRPATH / "outputs" / "colnames" / "clean_columns.json", "w"
        ) as f:
            json.dump(columns_dict, f, indent=1)

        copy = merged_dt.data.copy()

        # Fill in missing school names with the school long name or short name if necessary
        merged_dt.fill_school_names(column="school_long_name")
        merged_dt.fill_school_names(column="school_short_name")

        print(
            f"We filled in {merged_dt.data['school_name'].nunique() - copy['school_name'].nunique()} missing school names"
        )

        # Populate the merged data with the API columns
        merged_dt.populate_columns(
            identifier=["school_name"], columns=list(columns_API) + ["RCDTS"]
        )

        # Convert binary columns to Yes, No
        binary_columns = [ "has_transition_program", "has_bilingual_services", "has_refugee_services", 
                          "has_hearing_impairment_services", "has_visual_impairment_services"
        ]
        merged_dt.convert_to_binary(columns=binary_columns)

        # More cleaning
        merged_dt.data = merged_dt.data.dropna(how = "all")
        merged_dt.data.drop(columns = ["RCDTS", "school_short_name", "school_long_name", "school_type"], inplace = True)
        return

    elif version == "clean":
        merged_dt = import_data(
            filepath=DATA_DIRPATH / "clean" / "clean_panel.csv", raw=False
        )

        # Balance the panel
        merged_dt.balance_panel(years = [2019, 2020, 2021, 2022, 2023, 2024, 2025])

        # Fill in the missing ZIP codes
        merged_dt.populate_columns(identifier = ["school_name"], columns = ["zip"])

        # Input missing values
        context_columns = ["year", "zip"]
        columns_to_impute = ["enrollment", "ELA_proficiency", "math_proficiency", "science_proficiency", "sat_school_average", "graduation_rate", "graduation_rate4_year"]
        merged_dt.input_missing_values(columns = columns_to_impute, context = context_columns)

        # Save the updated merged data
        merged_dt.save_csv(DATA_DIRPATH / "clean" / "clean_panel.csv")

        return merged_dt
            
    else:
        raise ValueError(
            f"Invalid version: {version}. Choose from ['raw', 'intermediate', 'clean']"
        )

    


if __name__ == "__main__":
    clean_merged_data(version="clean")

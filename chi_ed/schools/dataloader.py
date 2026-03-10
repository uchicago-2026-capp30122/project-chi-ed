import pathlib
import pandas
from ..schools.data import Schools

COLNAMES_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "data" / "raw" / "colnames"


def _find_sheet(excel_file: pandas.ExcelFile, candidates: list[str]) -> str | None:
    """Return the first sheet name from candidates that exists in the Excel file, or None.
    I want to be very flexible to accommodate for different sheet names across years"""
    available = excel_file.sheet_names

    for sheet_name in candidates:
        if sheet_name in available:
            return sheet_name
    return None


def load_reports_card(filepath: pathlib.Path):
    """Load the reports card data from the given filepath.
    The filepath should be the path to the Excel file containing the reports card data for a given year."""
    if not filepath.exists():
        raise ValueError(f"File path does not exist: {filepath}")

    # Load the excel file
    excel_file = pandas.ExcelFile(filepath)

    # Try to find correct sheet names
    # NOTE: These are the sheet names across years (2019-2025)
    general_sheet = _find_sheet(excel_file, ["General"])
    scores_sheet = _find_sheet(excel_file, ["ELAMathScience", "ELA Math Science", "ELA and Math"])
    scores2_sheet = _find_sheet(excel_file, ["ELAMathScience (2)"])

    # Strict error handling for general sheet which contains metadata
    if general_sheet is None:
        raise ValueError(f"No 'General' sheet found in {filepath}")
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

    # Select & rename columns of interest
    # NOTE: I am using contains = False because we are using a unique columns dict across all datasets
    list_of_sheets = [general_dt] + other_sheets
    for sheet_data in list_of_sheets:
        sheet_data.select_columns(columns_to_keep, contains = False)
        sheet_data.rename_columns(columns_mapping)

    # Common columns across all sheets
    common_colnames = ["RCDTS", "school_name", "school_type", "county", "city", "district"]

    # Merge all sheets on the common columns
    # NOTE: Note how I denote dataframes with _df suffix and schools class objects with _dt suffix
    # This is a consistent naming convention I use across the project
    merged_df = general_dt.data
    for sheet_dt in other_sheets:
        merged_df = pandas.merge(
            merged_df, sheet_dt.data, on=common_colnames, how="left"
        )

    # Filter to "High Schools" and "Chicago" 
    merged_df = merged_df[merged_df["school_type"].str.strip().str.lower() == "high school"]
    merged_df = merged_df[merged_df["city"].str.strip().str.lower() == "chicago"]
    return Schools(merged_df)



COLUMNS_2025_REPORTS_CARDS = {
    "identifiers": {
        "RCDTS": "RCDTS",
        "School Name": "school_name",
        "District": "district",
        "City": "city",
        "County": "county",
        "School Type": "school_type",
    },
    "performance": {
        "% Math Proficiency": "math_proficiency",
        "% ELA Proficiency": "ELA_proficiency",
        "% Science Proficiency": "science_proficiency",
        "High School 4-Year Graduation Rate": "grad_rate",
    },
    "general": {
        "% Novice Teachers": "perc_novice_teachers",
        "Avg Teaching Exp": "avg_teaching_exp",
        "Pupil Teacher Ratio - High School": "pupil_teacher_ratio",
        "Avg Class Size - All Grades": "avg_class_size",
        "Chronic Absenteeism": "chronic_absenteeism",
        "High School Dropout Rate": "dropout_rate",
        "# Student Enrollment": "enrollment",
        "Children with Disabilities": "num_children_with_disabilities",
        "Teacher Attendance Rate": "teacher_attendance_rate",
    },
}

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
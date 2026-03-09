"""Data classes"""

import pandas


class Schools:
    """This is a temp design of schools class to facilitate operations on schools data
    I would rather pass in json files but for now I am storing pandas.DataFrames.
    """

    def __init__(self, schools_data: pandas.DataFrame):
        self.data = schools_data
        self.columns = schools_data.columns

        # Automatically correct RCDTS column
        if "RCDTS" not in self.columns:
            self.data["RCDTS"] = str(self.data["RCDTS"])

    def select_columns(self, columns: list, contains: bool = True):
        """Select columns of interest.
        Strict column mapping if necessary"""
        if contains:
            assert all(col in self.columns for col in columns), (
                f"All columns must be in the dataset: {columns}"
            )
            cols = columns
            self.data = self.data[cols]

        else:
            cols = [col for col in self.columns if col in columns]
            assert cols, f"No columns found in the dataset: {columns}"
            self.data = self.data[cols]

        self.columns = self.data.columns

    def filter(self, column: str, values: list):
        """Filter to specific values in a column.
        Example: filter to specific schools"""
        assert column in self.columns, f"Column not found in the data: {column}"
        assert all(value in self.data[column].values for value in values), (
            f"Some values are not present in the data: {values}. Column: {column}."
        )

        self.data = self.data[self.data[column].isin(values)]

    def rename_columns(self, mapping: dict):
        """Rename columns
        NOTE: This method is not an unecessary duplicate of pandas.DataFrame.rename() because it allows columns in mapping that are not in the data.
        This flexibility helps us use a unique columns dict across multiple datasets."""
        cols_mapping = {
            col: mapping[col] for col in mapping.keys() if col in self.columns
        }
        assert cols_mapping, f"No columns to rename found in the data: {mapping.keys()}"

        self.data.rename(columns=cols_mapping, inplace=True)
        self.columns = self.data.columns

    def set_year_attribute(self, year: int):
        """Set the year attribute and column"""
        self.data["year"] = year
        self.year = year

    def correct_school_names(self):
        """Use RCDTS to correct school names.
        I will just take the school name from the first occurrence of each RCDTS"""
        # Create a mapping of RCDTS to school name, a dict
        rcdts_school_mapping = (
            self.data.drop_duplicates(subset="RCDTS", keep="first")
            .set_index("RCDTS")["school_name"]
            .to_dict()
        )
        self.data["school_name"] = self.data["RCDTS"].map(rcdts_school_mapping)

    def fill_school_names(self, column: str):
        """Fill in school_name, if missing, with the value in column"""
        self.data["school_name"] = self.data["school_name"].fillna(self.data[column])

    def populate_columns(self, identifier: list[str], columns: list[str]):
        """For each column, populate the first non-null value per identifier group
        and fill it across all rows sharing those identifiers."""
        for column in columns:
            self.data[column] = self.data.groupby(identifier)[column].transform("first")

    def convert_to_binary(self, columns: str):
        """Convert binary columns to Yes, No"""
        for column in columns:
            self.data[column] = pandas.to_numeric(self.data[column], errors="coerce")
            self.data[column] = self.data[column].map({1.0: "Yes", 0.0: "No"})

    def assign_neighborhoods(self, mapping: dict):
        """Assign neighborhoods to schools based on the mapping"""
        self.data["neighborhood"] = self.data["school_name"].map(mapping)

    def save_csv(self, filepath: str):
        """Save the data to a csv file"""
        self.data.to_csv(filepath, index=False)
        print(f"Data successfully saved to {filepath}")


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

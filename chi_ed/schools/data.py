import pandas
from sklearn.impute import KNNImputer


class Schools:
    """This schools class facilitates operations on schools data (report cards particulary, 
    but some methods are general to pandas or polars dataframes).
    """
    def __init__(self, schools_data: pandas.DataFrame):
        self.data = schools_data
        self.columns = schools_data.columns

        # Automatically convert RCDTS column to string
        if "RCDTS" in self.columns:
            self.data["RCDTS"] = str(self.data["RCDTS"])

    def select_columns(self, columns: list, contains: bool = True):
        """Select columns of interest. Strict column mapping if necessary"""
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
        """Filter to specific values in a column"""
        assert column in self.columns, f"Column not found in the data: {column}"
        assert all(value in self.data[column].values for value in values), (
            f"Some values are not present in the data: {values}. Column: {column}."
        )
        self.data = self.data[self.data[column].isin(values)]

    def rename_columns(self, mapping: dict):
        """Rename columns.
        NOTE: This method is not a duplicate of pandas.DataFrame.rename() because it allows columns in mapping 
        that are not in the data. This flexibility helps us use a unique columns dict across multiple datasets."""
        cols_mapping = {
            col: mapping[col] for col in mapping.keys() if col in self.columns
        }
        assert cols_mapping, f"No columns to rename found in the data: {mapping.keys()}"

        self.data.rename(columns=cols_mapping, inplace=True)
        self.columns = self.data.columns

    def correct_school_names(self):
        """Use RCDTS to correct school names, taking the school name from the first occurrence of each RCDTS"""
        # Create a mapping of RCDTS to school name, a dict
        rcdts_school_mapping = (
            self.data.drop_duplicates(subset = "RCDTS", keep = "first")
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

    def balance_panel(self, years: list[int]):
        """Ensure every school_name has a row for every year in years."""
        schools = self.data["school_name"].unique()
        full_panel = pandas.MultiIndex.from_product(
            [schools, years],
            names = ["school_name", "year"],
        ).to_frame(index = False)
        self.data = full_panel.merge(self.data, on = ["school_name", "year"], how = "left")
        self.data = self.data.sort_values(["school_name", "year"]).reset_index(drop = True)
        self.columns = self.data.columns

    def input_missing_values(self, columns: list[str], context: list[str], n: int = 5):
        """Impute missing values for columns using KNN.
        Context columns inform neighbor distances but are not imputed."""
        all_cols = context + [column for column in columns if column not in context]
        df = self.data[all_cols].apply(pandas.to_numeric, errors="coerce")
        imputed = KNNImputer(n_neighbors=n).fit_transform(df)
        self.data[columns] = pandas.DataFrame(
            imputed, columns=all_cols, index=self.data.index
        )[columns]

    def save_csv(self, filepath: str):
        """Save the data to a csv file"""
        self.data.to_csv(filepath, index=False)
        print(f"Data successfully saved to {filepath}")

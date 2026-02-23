"""Data classes"""


class Schools():
    """This is a temp design of schools class to facilitate operations on schools data
    I would rather pass in json files but for now I am storing pandas.DataFrames.
    """
    def __init__(self, schools):
        self.schools = schools
        self.columns = schools.culumns

        def select_cols(self, columns: list):
            assert all(col in self.columns for col in columns), f"All columns must me in the dataset: {columns}"

            return self.schools[columns]
            
            



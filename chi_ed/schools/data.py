"""Data classes"""


class Schools():
    """This is a temp design of schools class to facilitate operations on schools data
    I would rather pass in json files but for now I am storing pandas.DataFrames.
    """
    def __init__(self, schools):
        self.data = schools
        self.columns = schools.columns
    def select_columns(self, columns: list, identifiers: bool = True):
        assert all(col in self.columns for col in columns), f"All columns must be in the dataset: {columns}"

        cols = list(columns)
        if identifiers:
            cols += ['RCDTS', 'school_name', 'district', 'city', 'county']
        return self.data[cols]

    def select_schools(self, names: list):
        assert all(name in self.data['school_name'].values for name in names), "Some school names are not present in the data"
        return self.data[self.data['school_name'].isin(names)]
            
            



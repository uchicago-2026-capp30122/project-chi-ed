"""Helper functions to generate pdfs"""

import typing
import pandas


class PDFdocument:
    def __init__(self, school1: str, school2: str):
        self.school1 = school1
        self.school2 = school2
        self.sections = {}

    def add_section(
        self,
        section: str,
        paragraph: str | typing.List[str] = None,
        figure: str = None,
        table: str = None,
    ):
        """Add a section to the document.

        figure and table are file paths to pre-generated images.
        """
        self.sections[section] = {
            "paragraph": paragraph,
            "figure": figure,
            "table": table,
        }

    def section(self, section: str):
        return self.sections[section]



def select_school(df: pandas.DataFrame, label: str) -> str:
    """Interactive menu to select a neighborhood then a school."""
    neighborhoods = sorted(df["neighborhood"].dropna().unique())
 
    
    print(f"\n----- Select {label} -----")
    
    # Numbered list of neighborhoods
    print("Neighborhoods:")
    for index, neighborhood in enumerate(neighborhoods, 1):
        print(f"  {index}. {neighborhood}")

    while True:
        choice = input(f"\nEnter neighborhood number for {label}: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(neighborhoods):
            break

        print(f"Invalid choice. Choose a number between 1 and {len(neighborhoods)} and try again.")


    neighborhood = neighborhoods[int(choice) - 1]
    schools = sorted(df.loc[df["neighborhood"] == neighborhood, "school_name"].unique())

    # Numbered list of schools
    print(f"\nSchools in {neighborhood}:")
    for index, school in enumerate(schools, 1):
        print(f"  {index}. {school}")

    while True:
        choice = input(f"\nEnter school number for {label}: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(schools):
            break

        print(f"Invalid choice. Choose a number between 1 and {len(schools)} and try again.")


    school = schools[int(choice) - 1]

    print(f"Selected: {school}")
    
    return school

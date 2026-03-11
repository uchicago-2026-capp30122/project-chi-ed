# Despite the filename, this script tests data scleaning of reports cards 
# and also the PDF Class object which stores sections of the PDF report.
# We will not test the actual PDF generation. 
import pandas 
from chi_ed.schools.data import Schools
from chi_ed.reports.pdfs_utils import PDFdocument


school_df = pandas.DataFrame({
    "school_name": ["A", "A", "A", "A", "B", "B", "C", "D", "E", "E"],
    "year": [1998, 1999, 2000, 2001, 1998, 1999, 1998, 1998, 2000, 1998],
    "free_meal_days": [None, 1, 7, None, 6, None, 5, 7, None, 4], 
    "elite": ["Yes", "Yes", None, "No", "No", None, None, "No", "Yes", "Yes"],
    "crisis": [110.4, None, None, 90, 21, 300, 48, 87, 110.4, 990]
}).astype({
    "school_name": "str",
    "year": "int",
    "free_meal_days": "Int64",
    "elite": "str",
    "crisis": "float64",
})

schools = Schools(school_df)


def test_imputer():
    """Test balancing filling missing values using sklearn.impute.KNNImputer"""
    schools.input_missing_values(columns = ["free_meal_days", "crisis"], context = ["year"])
    assert schools.data[["free_meal_days", "crisis"]].isnull().sum().sum() == 0, "There should be no missing values after imputation"


def test_balance_panel():
    """Test balancing the panel data"""
    n_schools = schools.data["school_name"].nunique()
    years = [1998, 1999, 2000, 2001]
    expected_len = n_schools * len(years)
    schools.balance_panel(years = years)
    assert len(schools.data) == expected_len, f"The balance panel should have {expected_len} rows"


def test_columns_renaming():
    """Test renaming columns"""
    schools.rename_columns(mapping = {"school_name": "school", "date": "year"})
    assert "school" in schools.data.columns and "school_name" not in schools.data.columns, "school_name column should be renamed to school"
    assert "date" not in schools.data.columns, "Renaming method should be flexible and ignore non-existent columns"



empty_pdf_doc = PDFdocument(school1 = "A", school2 = "B")

def test_empty_pdf():
    """Test there pdf object has a sections dictionary"""
    assert isinstance(empty_pdf_doc.sections, dict), "The sections dictionary should be a dictionary"
    assert len(empty_pdf_doc.sections) == 0, "The sections dictionary should be empty at initialization"


pdf_doc = PDFdocument(school1 = "A", school2 = "B")
pdf_doc.add_section(section = "Introduction", paragraph = "This is a test report")
pdf_doc.add_section(section = "Analysis", paragraph = "analysis is an analysis of a non-analyzed content", figure = None, table = None)
pdf_doc.add_section(section = "Conclusion", paragraph = "Trust the process", figure = None, table = None)
pdf_doc.add_section(section = "References", paragraph = "UChicago 2026", figure = None, table = None)
pdf_doc.add_section(section = "Appendix", paragraph = "It's been a good ride!!!", figure = None, table = None)


def test_section_access():
    """Test accessing sections of the pdf object"""
    analysis_text = pdf_doc.section("Analysis")
    assert analysis_text, "The Analysis section contains no paragraph text"
    assert pdf_doc.section("Conclusion")["paragraph"] == "Trust the process", "The Conclusion section should have the correct paragraph"
    assert pdf_doc.section("References")["paragraph"] == "UChicago 2026", "The References section should have the correct paragraph"
    assert pdf_doc.section("Appendix")["figure"] is None, "The Appendix section should have no figure, when none added"
    assert pdf_doc.section("Appendix")["table"] is None, "The Appendix section should have no table, when none added"
    
    
    
    
# Import all other modules in this file and run everything here
import sys
import webbrowser
import pandas
import pathlib
from chi_ed.spatial.dashboard import app
from chi_ed.reports.reports import create_report, DATA_DIRPATH
from chi_ed.reports.pdfs_utils import select_school

REPORT_DIRPATH = pathlib.Path(__file__).parent / "REPORT.pdf"

if __name__ == "__main__":
    # First let's make sure the data exists
    if not DATA_DIRPATH.exists():
        raise FileNotFoundError(
            f"Data file not found at {DATA_DIRPATH}. \nThis is on us not you, sorry! Try again later."
        )

    if len(sys.argv) != 2:
        raise ValueError("Usage: python -m chi_ed `dashboard | report | clean`")

    task = str(sys.argv[1])

    if task == "dashboard":
        app.run(debug=True)

    elif task == "report":
        clean_panel_df = pandas.read_csv(DATA_DIRPATH)
        school1 = select_school(clean_panel_df, "1st school")
        school2 = select_school(clean_panel_df, "2nd school")

        print(f"\nGenerating report for {school1} & {school2}...")

        create_report(
            df=clean_panel_df,
            school1=school1,
            school2=school2,
            output_filepath=REPORT_DIRPATH,
        )
        print(f"Report saved to {REPORT_DIRPATH}")

        # Open the report in the default browser
        webbrowser.open(REPORT_DIRPATH.as_uri())

import subprocess
import re
import math
import json
import pathlib
import pandas
from .pdfs_utils import PDFdocument
from .mapping import plot_bar_graph, plot_time_series
from .tabulation import summary_table

VARIABLES_DIRPATH = pathlib.Path(__file__).parent.resolve() / "variables"
TEMPLATE_PATH = pathlib.Path(__file__).parent.resolve() / "render_report.md"
DATA_DIRPATH = (
    pathlib.Path(__file__).parent.parent.parent.resolve()
    / "data"
    / "clean"
    / "clean_panel.csv"
)
REPORTS_DIRPATH = pathlib.Path(__file__).parent.parent.parent.resolve() / "reports"
FIGURES_DIRPATH = REPORTS_DIRPATH / "figures"
TABLES_DIRPATH = REPORTS_DIRPATH / "tables"


def render_report(PDF_doc: PDFdocument, output_filepath: pathlib.Path):
    """Read render_report.md, replace placeholders with pre-generated image
    paths from the PDFdocument, and convert to PDF via pandoc."""

    with open(TEMPLATE_PATH, "r") as f:
        template = f.read()

    template = template.replace("{{school1}}", PDF_doc.school1)
    template = template.replace("{{school2}}", PDF_doc.school2)

    # Replace placeholders with pre-generated image and table paths
    for section_name, content in PDF_doc.sections.items():
        figure_path = content.get("figure")
        table_path = content.get("table")
        if figure_path:
            template = template.replace(
                f"{{{{figure:{section_name}}}}}", f"![]({figure_path})\\ "
            )
        if table_path:
            if str(table_path).endswith(".tex"):
                template = template.replace(
                    f"{{{{table:{section_name}}}}}", f"\\input{{{table_path}}}"
                )
            else:
                template = template.replace(
                    f"{{{{table:{section_name}}}}}", f"![]({table_path})\\ "
                )

    # Set the school addresses
    template = template.replace("{{school1_address}}", PDF_doc.school1_address)
    template = template.replace("{{school2_address}}", PDF_doc.school2_address)

    # Render the report and save it in the reports directory
    output_filepath = pathlib.Path(output_filepath)
    output_filepath.parent.mkdir(parents=True, exist_ok=True)

    # Convert to markdown and save
    md_path = output_filepath.with_suffix(".md")
    with open(md_path, "w") as f:
        f.write(template)

    # Convert to PDF and save
    subprocess.run(
        ["pandoc", str(md_path), "-o", str(output_filepath), "--pdf-engine=pdflatex"],
        check=True,
    )
    # Remove the markdown file
    md_path.unlink()


def load_variables(filename: str) -> dict:
    """Load a variable mapping JSON from the variables directory."""
    with open(VARIABLES_DIRPATH / filename, "r") as f:
        return json.load(f)


def generate_figure(
    df: pandas.DataFrame,
    variables: dict,
    school1: str,
    school2: str,
    filepath: pathlib.Path,
    year: int = 2025,
) -> str:
    """Generate a bar plot grid, save to filepath, and return the path."""
    filepath = pathlib.Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    n = len(variables)
    ncols = min(n, 2)
    nrows = math.ceil(n / ncols)
    plot_bar_graph(
        df,
        variables,
        school1,
        school2,
        nrows=nrows,
        ncols=ncols,
        year=year,
        filepath=filepath,
    )
    return str(filepath)


def generate_time_series(
    df: pandas.DataFrame,
    variables: dict,
    school1: str,
    school2: str,
    filepath: pathlib.Path,
) -> str:
    """Generate a time series plot, save to filepath, and return the path."""
    filepath = pathlib.Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    plot_time_series(df, variables, school1, school2, filepath=filepath)
    return str(filepath)


def generate_table(
    df: pandas.DataFrame,
    section: str,
    variables: dict,
    school1: str,
    school2: str,
    filepath: pathlib.Path,
    round_to: int = 0,
    display_chicago: bool = True,
) -> str:
    """Generate a summary table, save to filepath, and return the path."""
    filepath = pathlib.Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    summary_table(
        df,
        section,
        variables,
        school1,
        school2,
        filepath=filepath,
        round_to=round_to,
        display_chicago=display_chicago,
    )
    return str(filepath)


def generate_school_address(df: pandas.DataFrame, school: str) -> str:
    """Generate a US-style address for a school."""
    street_address = df.loc[df["school_name"] == school, "address_street"].values[0]
    city = df.loc[df["school_name"] == school, "city"].values[0]
    zip_code = df.loc[df["school_name"] == school, "zip"].values[0]
    return f"{school}, {street_address}, {city}, Illinois {int(zip_code)}"


clean_panel_df = pandas.read_csv(DATA_DIRPATH)


def create_report(
    school1: str, school2: str, output_filepath: pathlib.Path, year: int = 2025
):
    """Create and render a full comparison report for two schools."""
    PDF_doc = PDFdocument(school1, school2)

    PDF_doc.add_section(
        "Overview",
        figure=generate_time_series(
            clean_panel_df,
            load_variables("overview.json"),
            school1,
            school2,
            filepath=FIGURES_DIRPATH / f"overview_{school1}_{school2}.png",
        ),
    )

    PDF_doc.add_section(
        "Academic Performance",
        figure=generate_figure(
            clean_panel_df,
            load_variables("academic.json"),
            school1,
            school2,
            filepath=FIGURES_DIRPATH / f"academics_{school1}_{school2}.png",
            year=year,
        ),
    )

    PDF_doc.add_section(
        "Enrollment & Demographics",
        table=generate_table(
            clean_panel_df,
            "Enrollment & Demographics",
            load_variables("enrollment.json"),
            school1,
            school2,
            filepath=TABLES_DIRPATH / f"enrollment_{school1}_{school2}.tex",
            round_to=0,
            display_chicago=True,
        ),
    )

    PDF_doc.add_section(
        "Faculty & Attendance",
        table=generate_table(
            clean_panel_df,
            "Faculty & Attendance",
            load_variables("faculty.json"),
            school1,
            school2,
            filepath=TABLES_DIRPATH / f"faculty_{school1}_{school2}.tex",
            round_to=1,
            display_chicago=True,
        ),
    )

    PDF_doc.add_section(
        "Ratings",
        table=generate_table(
            clean_panel_df,
            "Ratings",
            load_variables("ratings.json"),
            school1,
            school2,
            filepath=TABLES_DIRPATH / f"ratings_{school1}_{school2}.tex",
            round_to=0,
            display_chicago=False,
        ),
    )

    PDF_doc.add_section(
        "Infrastructure & Services",
        table=generate_table(
            clean_panel_df,
            "Infrastructure & Services",
            load_variables("infrastructure.json"),
            school1,
            school2,
            filepath=TABLES_DIRPATH / f"infrastructure_{school1}_{school2}.tex",
            round_to=0,
            display_chicago=False,
        ),
    )

    PDF_doc.school1_address = generate_school_address(clean_panel_df, school1)
    PDF_doc.school2_address = generate_school_address(clean_panel_df, school2)

    render_report(PDF_doc, output_filepath)


# TODO: Create cache file to retrieve the report if it already exists
if __name__ == "__main__":
    panel_df = pandas.read_csv(DATA_DIRPATH)

    with open("schools.json", "w") as f:
        json.dump(panel_df["school_name"].unique().tolist(), f, indent=1)

    school1 = "Amundsen High School"
    school2 = "Back of The Yards IB HS"

    output_filepath = REPORTS_DIRPATH / f"{school1}_{school2}.pdf"

    create_report(
        df=panel_df,
        school1=school1,
        school2=school2,
        output_filepath=output_filepath,
        year=2025,
    )

"""Helper functions to generate pdfs"""

import typing
import pathlib


class PDFdocument:
    def __init__(self, school1: str, school2: str):
        self.school1 = school1
        self.school2 = school2
        self.sections = {}

    def add_title(self, title: str):
        self.title = title

    def add_overview(self, overview: str):
        self.overview = overview

    def add_section(self, section: str, paragraph: typing.List[str], figure: typing.List[str], table: typing.List[str]):
        self.sections[section] = {
            "paragraph": paragraph,
            "figure": figure,
            "table": table
        }

    def section(self, section: str):
        return self.sections[section]

    def filepath(self):
        filename = f"report_{self.school1}_{self.school2}.pdf"
        return pathlib.Path("outputs/pdfs") / filename

    def save(self):
        self.filepath.write_text(self.content)





"""Helper functions to generate pdfs"""

import typing
import pathlib


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

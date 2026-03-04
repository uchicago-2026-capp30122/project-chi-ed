import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
from ..viz.pdfs_utils import PDFdocument


def render_report(doc: PDFdocument, output_path: str = None):
    """Renders a PDFdocument to a PDF file using matplotlib's PdfPages"""
    if output_path is None:
        output_path = str(doc.filepath())

    PAGE_WIDTH, PAGE_HEIGHT = 8.5, 11
    MARGIN = 0.07
    IMG_HEIGHT = 0.45

    with PdfPages(output_path) as pdf:
        fig, ax = plt.subplots(figsize = (PAGE_WIDTH, PAGE_HEIGHT))
        ax.axis("off")
        y_cursor = 1.0 - MARGIN

        def new_page():
            nonlocal fig, ax, y_cursor
            pdf.savefig(fig)
            plt.close(fig)
            fig, ax = plt.subplots(figsize=(PAGE_WIDTH, PAGE_HEIGHT))
            ax.axis("off")
            y_cursor = 1.0 - MARGIN

        def ensure_space(needed):
            nonlocal y_cursor
            if y_cursor - needed < MARGIN:
                new_page()

        def add_text(text, fontsize = 10, fontweight = "normal", style = "normal", spacing = 0.04):
            nonlocal y_cursor
            ensure_space(spacing + 0.02)
            ax.text(
                    MARGIN, 
                    y_cursor, 
                    text, 
                    fontsize = fontsize, 
                    fontweight = fontweight,
                    style = style, 
                    va = "top", 
                    transform = ax.transAxes,
                    horizontalalignment = "left", 
                    wrap = True)
            y_cursor -= spacing

        def add_image(img_path):
            nonlocal y_cursor
            ensure_space(IMG_HEIGHT + 0.03)
            img = mpimg.imread(img_path)
            img_height, img_width = img.shape[:2]
            aspect = img_width / img_height
            img_width = 1.0 - 2 * MARGIN
            img_height = img_width / aspect * (PAGE_WIDTH / PAGE_HEIGHT)
            inset_ax = fig.add_axes([MARGIN, y_cursor - img_height, img_width, img_height])
            inset_ax.imshow(img)
            inset_ax.axis("off")
            y_cursor -= img_height + 0.03

        # Title
        add_text(doc.title, fontsize = 22, fontweight = "bold", spacing = 0.06)
        add_text(f"{doc.school1} & {doc.school2}", fontsize = 13, style = "italic", spacing = 0.05)

        # Overview
        if hasattr(doc, "overview") and doc.overview:
            add_text("Overview", fontsize = 16, fontweight = "bold", spacing = 0.05)
            add_text(doc.overview, fontsize = 10, spacing = 0.06)

        # Sections
        for section_name, content in doc.sections.items():
            paragraph = content.get("paragraph")
            figure = content.get("figure")
            table = content.get("table")

            add_text(section_name, fontsize = 14, fontweight = "bold", spacing = 0.05)

            if paragraph:
                text = "\n".join(paragraph) if isinstance(paragraph, list) else paragraph
                add_text(text, fontsize = 10, spacing = 0.06)

            if figure:
                fig_path = figure[0] if isinstance(figure, list) else figure
                add_image(fig_path)

            if table:
                tbl_path = table[0] if isinstance(table, list) else table
                add_image(tbl_path)

        pdf.savefig(fig)
        plt.close(fig)

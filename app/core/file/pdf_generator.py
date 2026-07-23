import os
import tempfile
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from pathlib import Path


class PDFGenerator:

    @staticmethod
    def generate(
        file_name: str,
        project_name: str,
        content,
    ) -> str:
        """
        content:
            dict  -> Table
            str   -> Paragraph
        """

        print("-----------------------------------------------")
        print("file_name",file_name)
        print("project_name",project_name)

        
        main_title = project_name +"-"+ file_name.split(".")[0]
        
        title = f"{main_title} - Analysis"
        pdf_name = f"{main_title}-Analysis.pdf"

        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        output_dir = tempfile.gettempdir()

        pdf_path = os.path.join(output_dir, pdf_name)

        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        
        styles = getSampleStyleSheet()
        
        
        elements = []

        elements.append(
            Paragraph(f"<h3>{title}</h3>", styles["Title"])
        )

        elements.append(
            Paragraph(
                f"Generated on {date}",
                styles["BodyText"]
            )
        )

        elements.append(Spacer(1, 20))

        # -------------------------
        # Dictionary
        # -------------------------
        if isinstance(content, dict):

            data = [["Item", "Value"]]

            for key, value in content.items():
                data.append([
                    str(key),
                    str(value)
                ])

            table = Table(data)

            table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ])
            )

            elements.append(table)

        # -------------------------
        # Text
        # -------------------------
        else:

            text = str(content).replace("\n", "<br/>")

            elements.append(
                Paragraph(text, styles["BodyText"])
            )

        doc.build(elements)


        print("pdf_path",pdf_path)
        print("pdf_name", pdf_name)
        print("-----------------------------------------------")

        return pdf_path
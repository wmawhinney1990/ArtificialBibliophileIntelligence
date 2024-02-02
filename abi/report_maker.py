import os
from pathlib import Path
from typing import Union, List

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import StyleSheet1, ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER       #TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from abi.notes import BasicNotes as Notes

all = ["ReportMaker"]

class ReportMaker:
    """
    Report making utility class
    """

    @classmethod
    def ensure_pdf(cls, name: str) -> str:
        if name.endswith(".pdf") is False:
            return f"{name}.pdf"
        return name

    @classmethod
    def check_dir(cls, directory: Union[str, Path]):
        if Path(directory).is_dir() is False:
            raise NotADirectoryError(f"{str(notes_dir)!r} is not a valid directory.")

    @classmethod
    def get_styles(cls) -> StyleSheet1:

        stylesheet = StyleSheet1()

        title_style = ParagraphStyle("Title", fontName="Helvetica", fontSize=22, alignment=TA_CENTER, spaceAfter=10)
        body_style = ParagraphStyle("BodyText", fontName="Times-Roman", fontSize=12)
        bullet_style = ParagraphStyle("Bullet", fontName="Helvetica", leftIndent=17, fontSize=9)

        stylesheet.add(title_style, alias="title")
        stylesheet.add(body_style, alias="body")
        stylesheet.add(bullet_style, alias="bullet")

        return stylesheet

    @classmethod
    def get_notes_from_dir(cls, notes_dir, include_qa=False) -> List[tuple]:
        notes = { filename: Notes.from_pickle(notes_dir/filename) for filename in os.listdir(notes_dir) if filename.endswith(".pkl") }
        if include_qa:
            return [ (n, str(notes[n].summary), notes[n].points, notes[n].qa) for n in sorted(list(notes.keys())) ]
        return [ (n, str(notes[n].summary), notes[n].points) for n in sorted(list(notes.keys())) ]

    @classmethod
    def create_notes_document(cls, report_path: Union[str, Path], chunks, styles, include_qa=False):
        flowables = [ ]
        for chunk in chunks:

            title = Paragraph(chunk[0], styles['Title'])
            summary = Paragraph(chunk[1], styles['BodyText'])
            points = [ Paragraph(f"<bullet>&bull;</bullet>{point}", styles['Bullet']) for point in chunk[2] ]
            if include_qa:
                qa_table = Table([["Question", "Answer"]] + [ [k, v] for k, v in chunk[3].items() ])
                tblstyle = TableStyle([ ('BACKGROUND', (0, 0), (-1, 0), colors.blue) ])
                qa_table.setStyle(tblstyle)

            flowables.append(title)
            flowables.append(Spacer(1, .2*inch))
            flowables.append(summary)
            flowables.append(Spacer(1, .2*inch))
            flowables.extend(points)
            if include_qa:
                flowables.append(Spacer(1, .2*inch))
                flowables.append(qa_table)
            flowables.append(Spacer(1, .5*inch))

        SimpleDocTemplate(str(report_path), pagesize=letter).build(flowables)

    @classmethod
    def make_report_from_notes(cls, name: str, notes_dir: Path) -> Path:
        cls.check_dir(notes_dir)
        report_path = Path(notes_dir) / cls.ensure_pdf(name)

        styles = cls.get_styles()
        chunks = cls.get_notes_from_dir(notes_dir, include_qa=False)
        cls.create_notes_document(report_path, chunks, styles, include_qa=False)

        return f"Report saved to {str(report_path)!r}"
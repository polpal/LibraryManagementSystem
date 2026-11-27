from datetime import date
import csv
from io import StringIO
from io import BytesIO
from operator import index

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

from app.models import Transaction
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import ParagraphStyle
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from banglapdf import (
    register_fonts,
    BanglaParagraph,
    bangla_style,
)

# Register fonts for English, Bengali and Hindi PDF text.

FONT_DIR = Path(__file__).resolve().parent.parent / "static" / "fonts"
# Register combined English and Bengali font.

register_fonts(
    latin_regular=str(FONT_DIR / "NotoSans-Regular.ttf"),
    latin_bold=str(FONT_DIR / "NotoSans-Bold.ttf"),
    bangla_regular=str(FONT_DIR / "NotoSansBengali-Regular.ttf"),
    bangla_bold=str(FONT_DIR / "NotoSansBengali-Bold.ttf"),
)

pdfmetrics.registerFont(
    TTFont(
        "NotoSans",
        str(FONT_DIR / "NotoSans-Regular.ttf"),
        shapable=True,
    )
)

pdfmetrics.registerFont(
    TTFont(
        "NotoSansBengali",
        str(FONT_DIR / "NotoSansBengali-Regular.ttf"),
        shapable=True,
    )
)

pdfmetrics.registerFont(
    TTFont(
        "NotoSansDevanagari",
        str(FONT_DIR / "NotoSansDevanagari-Regular.ttf"),
        shapable=True,
    )
)


def get_issued_books_report():
    """Return all transactions for books that have not been returned."""

    return (
        Transaction.query.filter(Transaction.return_date.is_(None))
        .order_by(Transaction.due_date.asc())
        .all()
    )


def get_overdue_books_report():
    """Return active transactions whose due date has passed."""

    today = date.today()

    return (
        Transaction.query.filter(
            Transaction.return_date.is_(None),
            Transaction.due_date < today,
        )
        .order_by(Transaction.due_date.asc())
        .all()
    )


def get_report_summary():
    """Return summary counts for the library reports."""

    today = date.today()

    total_issued = Transaction.query.filter(Transaction.return_date.is_(None)).count()

    total_overdue = Transaction.query.filter(
        Transaction.return_date.is_(None),
        Transaction.due_date < today,
    ).count()

    issued_today = Transaction.query.filter(Transaction.issue_date == today).count()

    return {
        "total_issued": total_issued,
        "total_overdue": total_overdue,
        "issued_today": issued_today,
    }


def get_filtered_report(report_type, start_date, end_date):
    """Return report transactions filtered by report type and date range."""

    query = Transaction.query

    if report_type == "issued":

        query = query.filter(
            Transaction.return_date.is_(None),
            Transaction.issue_date >= start_date,
            Transaction.issue_date <= end_date,
        )

        query = query.order_by(Transaction.issue_date.desc())

    elif report_type == "overdue":

        today = date.today()

        query = query.filter(
            Transaction.return_date.is_(None),
            Transaction.due_date < today,
            Transaction.due_date >= start_date,
            Transaction.due_date <= end_date,
        )

        query = query.order_by(Transaction.due_date.asc())

    elif report_type == "returned":

        query = query.filter(
            Transaction.return_date.isnot(None),
            Transaction.return_date >= start_date,
            Transaction.return_date <= end_date,
        )

        query = query.order_by(Transaction.return_date.desc())

    elif report_type == "history":

        query = query.filter(
            Transaction.issue_date >= start_date,
            Transaction.issue_date <= end_date,
        )

        query = query.order_by(Transaction.issue_date.desc())

    else:
        raise ValueError("Invalid report type.")

    return query.all()


def generate_report_csv(report_data):
    """Generate CSV content from filtered report transactions."""

    output = StringIO()

    writer = csv.writer(output)

    # CSV column headings.
    writer.writerow(
        [
            "Transaction No.",
            "Accession No.",
            "Book Name",
            "Member No.",
            "Member Name",
            "Issue Date",
            "Due Date",
            "Return Date",
        ]
    )

    if not report_data:

        writer.writerow(["No data available for the selected report and date range."])

    else:

        for transaction in report_data:

            writer.writerow(
                [
                    transaction.transaction_no,
                    transaction.book.accession_no,
                    transaction.book.book_name,
                    transaction.member.member_no,
                    transaction.member.name,
                    transaction.issue_date,
                    transaction.due_date,
                    transaction.return_date or "",
                ]
            )

    return output.getvalue()


def generate_report_excel(report_data):
    """Generate an Excel workbook from filtered report transactions."""

    workbook = Workbook()

    worksheet = workbook.active
    worksheet.title = "Library Report"

    # Report headings.
    headers = [
        "Transaction No.",
        "Accession No.",
        "Book Name",
        "Member No.",
        "Member Name",
        "Issue Date",
        "Due Date",
        "Return Date",
    ]

    worksheet.append(headers)

    # Format the heading row.
    for cell in worksheet[1]:

        cell.font = Font(bold=True, color="FFFFFF")

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="1F4E78",
        )

        cell.alignment = Alignment(horizontal="center")

    # Add report records.
    if not report_data:

        worksheet.append(["No data available for the selected report and date range."])

    else:

        for transaction in report_data:

            worksheet.append(
                [
                    transaction.transaction_no,
                    transaction.book.accession_no,
                    transaction.book.book_name,
                    transaction.member.member_no,
                    transaction.member.name,
                    transaction.issue_date,
                    transaction.due_date,
                    transaction.return_date or "",
                ]
            )

    # Set column widths.
    column_widths = [18, 18, 30, 18, 25, 15, 15, 15]

    for index, width in enumerate(column_widths, start=1):

        worksheet.column_dimensions[
            worksheet.cell(row=1, column=index).column_letter
        ].width = width

    # Keep headings visible while scrolling.
    worksheet.freeze_panes = "A2"

    # Enable filtering when records exist.
    if report_data:

        worksheet.auto_filter.ref = worksheet.dimensions

    # Save workbook in memory.
    output = BytesIO()

    workbook.save(output)

    output.seek(0)

    return output


def get_multilingual_font(value):
    """Identify the script used in the text."""

    text = str(value)

    if any(0x0980 <= ord(char) <= 0x09FF for char in text):
        return "Bangla"

    if any(0x0900 <= ord(char) <= 0x097F for char in text):
        return "NotoSansDevanagari"

    return "NotoSans"


def generate_report_pdf(report_data, report_type, start_date, end_date):
    """Generate a full-width, formatted PDF library report."""

    output = BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=landscape(A4),
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    elements = []

    # Report title.
    title = report_type.replace("_", " ").title() + " Report"

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="NotoSans",
    )

    elements.append(Paragraph(title, title_style))

    elements.append(Spacer(1, 5 * mm))

    # Report period.
    date_range = (
        f"Period: {start_date.strftime('%d-%m-%Y')} "
        f"to {end_date.strftime('%d-%m-%Y')}"
    )

    elements.append(Paragraph(date_range, styles["Normal"]))

    elements.append(Spacer(1, 8 * mm))

    # Table text styles.
    header_style = ParagraphStyle(
        "ReportHeader",
        fontName="NotoSans",
        fontSize=7,
        leading=9,
        textColor=colors.white,
        alignment=1,
        wordWrap="CJK",
    )

    body_style = ParagraphStyle(
        "ReportBody",
        fontName="NotoSans",
        fontSize=7,
        leading=9,
        alignment=1,
        wordWrap="CJK",
    )

    left_style = ParagraphStyle(
        "ReportBodyLeft",
        parent=body_style,
        alignment=0,
    )

    # Table headings.
    headers = [
        "Transaction No.",
        "Accession No.",
        "Book Name",
        "Member No.",
        "Member Name",
        "Issue Date",
        "Due Date",
        "Return Date",
    ]

    table_data = [[Paragraph(header, header_style) for header in headers]]

    # Add report records.
    if report_data:

        for transaction in report_data:

            row = [
                transaction.transaction_no,
                transaction.book.accession_no,
                transaction.book.book_name,
                transaction.member.member_no,
                transaction.member.name,
                transaction.issue_date.strftime("%d-%m-%Y"),
                transaction.due_date.strftime("%d-%m-%Y"),
                (
                    transaction.return_date.strftime("%d-%m-%Y")
                    if transaction.return_date
                    else "-"
                ),
            ]

            formatted_row = []

            for index, value in enumerate(row):

                cell_style = left_style if index in (2, 4) else body_style

                cell_font = get_multilingual_font(value)

                cell_style = ParagraphStyle(
                    f"ReportCell{index}",
                    parent=cell_style,
                    fontName=cell_font,
                    shaping=1,
                )

                cell_text = str(value)

                if cell_font == "Bangla":
                    cell_paragraph = BanglaParagraph(
                        cell_text,
                        bangla_style(
                            fontSize=cell_style.fontSize,
                            leading=cell_style.leading,
                            textColor=cell_style.textColor,
                            alignment=cell_style.alignment,
                        ),
                    )
                else:
                    cell_paragraph = Paragraph(
                        escape(cell_text),
                        cell_style,
                    )

                formatted_row.append(cell_paragraph)

            table_data.append(formatted_row)

    else:

        table_data.append(
            [
                Paragraph(
                    "No data available for the selected report and date range.",
                    body_style,
                )
            ]
            + [""] * 7
        )

    # Calculate available page width.
    available_width = landscape(A4)[0] - document.leftMargin - document.rightMargin

    # Allocate the entire printable width.
    column_ratios = [
        0.11,  # Transaction No.
        0.10,  # Accession No.
        0.21,  # Book Name
        0.10,  # Member No.
        0.16,  # Member Name
        0.10,  # Issue Date
        0.10,  # Due Date
        0.12,  # Return Date
    ]

    column_widths = [available_width * ratio for ratio in column_ratios]

    # Create full-width table.
    report_table = Table(
        table_data,
        colWidths=column_widths,
        repeatRows=1,
        hAlign="LEFT",
    )

    report_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#EAF0F6")],
                ),
                (
                    ("SPAN", (0, 1), (-1, 1))
                    if not report_data
                    else ("ALIGN", (0, 0), (-1, -1), "CENTER")
                ),
            ]
        )
    )

    elements.append(report_table)

    # Page numbering.
    def add_page_number(canvas, document):

        canvas.saveState()

        canvas.setFont("NotoSans", 8)

        canvas.drawRightString(
            landscape(A4)[0] - 15 * mm,
            8 * mm,
            f"Page {document.page}",
        )

        canvas.restoreState()

    # Generate PDF.
    document.build(
        elements,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    output.seek(0)

    return output

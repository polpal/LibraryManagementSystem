from datetime import date
import csv
from io import StringIO
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

from app.models import Transaction


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

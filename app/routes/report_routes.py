from datetime import date

from flask import Blueprint, render_template, request, flash
from flask_login import login_required

from app.utils.decorators import role_required
from app.services.report_service import (
    get_issued_books_report,
    get_overdue_books_report,
    get_report_summary,
    get_filtered_report,
)

report_bp = Blueprint("report", __name__, url_prefix="/reports")


@report_bp.route("/")
@login_required
@role_required("Admin", "Librarian")
def reports():

    today = date.today()

    # Default date range: first day of this month to today.
    default_start_date = today.replace(day=1)

    report_type = request.args.get("report_type", "issued")
    start_date_value = request.args.get("start_date")
    end_date_value = request.args.get("end_date")

    try:
        start_date = (
            date.fromisoformat(start_date_value)
            if start_date_value
            else default_start_date
        )

        end_date = date.fromisoformat(end_date_value) if end_date_value else today

        if start_date > end_date:
            raise ValueError("Start date cannot be later than end date.")

        report_data = get_filtered_report(
            report_type,
            start_date,
            end_date,
        )

    except ValueError as error:

        flash(str(error), "danger")

        report_type = "issued"
        start_date = default_start_date
        end_date = today

        report_data = get_filtered_report(
            report_type,
            start_date,
            end_date,
        )

    # Overall library summary.
    summary = get_report_summary()

    # Retain existing data while the template is being upgraded.
    issued_books = get_issued_books_report()
    overdue_books = get_overdue_books_report()

    return render_template(
        "reports/reports.html",
        issued_books=issued_books,
        overdue_books=overdue_books,
        summary=summary,
        report_data=report_data,
        report_type=report_type,
        start_date=start_date,
        end_date=end_date,
    )

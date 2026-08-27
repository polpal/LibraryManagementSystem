from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import admin_required


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@login_required
def dashboard():

    return render_template(
        "dashboard/dashboard.html"
    )
    
@dashboard_bp.route("/admin-test")
@login_required
@admin_required
def admin_test():

    return "Admin Access Granted"
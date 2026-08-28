from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
        
        if not current_user.is_authenticated:
            abort(401)

        if current_user.role != "Admin":
            abort(403)

        return func(*args, **kwargs)

    return decorated_function


from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for


def role_required(*roles):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if current_user.role not in roles:

                flash(
                    "You are not authorized to access this page.",
                    "danger"
                )

                return redirect(
                    url_for("dashboard.dashboard")
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
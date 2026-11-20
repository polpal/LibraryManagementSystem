import secrets
import hmac

from ..models import db


def generate_session_token():
    """
    Generate a cryptographically secure session token.
    Returns a 64-character hexadecimal string.
    """

    return secrets.token_hex(32)


def is_session_valid(user, browser_token):
    """
    Check whether the browser token matches
    the active token stored in the database.
    """

    if not user or not browser_token:
        return False

    if not user.active_session_token:
        return False

    return hmac.compare_digest(user.active_session_token, browser_token)


def activate_session(user, token):
    """
    Store the new active session token in the database.
    """

    try:
        user.active_session_token = token
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise


def invalidate_session(user, browser_token):
    """
    Clear the active token only if it belongs
    to the requesting browser.
    """

    if not is_session_valid(user, browser_token):
        return False

    try:
        user.active_session_token = None
        db.session.commit()
        return True

    except Exception:
        db.session.rollback()
        raise

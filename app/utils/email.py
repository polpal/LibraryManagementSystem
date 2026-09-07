from flask_mail import Message

from app.extensions import mail
from flask import current_app


def send_reset_email(user):

    token = user.get_reset_token()

    reset_url = (
        f"http://127.0.0.1:5000"
        f"/reset-password/{token}"
    )

    msg = Message(
        subject="Password Reset Request",
        recipients=[user.email]
    )

    msg.body = f"""
    Hello {user.username},

    To reset your password visit:

    {reset_url}

    This link expires in 1 hour.

    If you did not request this reset,
    please ignore this email.
"""
    print("=== MAIL CONFIG ===")
    print(current_app.config["MAIL_USERNAME"])
    print(current_app.config["MAIL_DEFAULT_SENDER"])
    print(current_app.config["MAIL_SERVER"])
    print(current_app.config["MAIL_PORT"])
    print("===================")
    mail.send(msg)
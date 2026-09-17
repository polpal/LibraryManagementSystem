from flask_mail import Message

from app.extensions import mail
from flask import current_app


def send_reset_email(user):

    token = user.get_reset_token()

    reset_url = f"http://127.0.0.1:5000" f"/reset-password/{token}"

    msg = Message(subject="Password Reset Request", recipients=[user.email])

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


def send_member_welcome_email(member, temporary_password):

    msg = Message(
        subject="Welcome to Railway Library",
        recipients=[member.email],
    )

    msg.body = f"""
Hello {member.name},

Welcome to Railway Library.

Your library membership has been successfully created.

Membership Details
------------------
Member Number : {member.member_no}
Name          : {member.name}
Department    : {member.department}
Designation   : {member.designation}
Email         : {member.email}

Login Details
-------------
Username           : {member.member_no}
Temporary Password : {temporary_password}

Please use the above credentials to log in to the Railway Library system.

For security reasons, you will be required to change
your password when you log in for the first time.

Please do not share your password with anyone.

Regards,
Railway Library
"""

    mail.send(msg)

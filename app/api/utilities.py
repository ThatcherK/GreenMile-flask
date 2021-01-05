import os
import random
import string

from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))

def send_invite_email(invite_code, email, frontend_url):
    message = Mail(
        from_email=f'{current_app.config.get("SENDGRID_SENDER_MAIL")}',
        to_emails=f"{email}",
        subject="Greenmile Platform Invite",
        html_content=f"""<p>Hello,
        You have been invited to the Greenmile platform with this code<br>
        <strong>{invite_code}</strong><br><br>Please copy the code, 
        follow this link {frontend_url} to sign up! </p>""",
    )
    try:
        sg = SendGridAPIClient(current_app.config.get("SENDGRID_API_KEY"))
        response = sg.send(message)

    except Exception as e:
        return repr(e)
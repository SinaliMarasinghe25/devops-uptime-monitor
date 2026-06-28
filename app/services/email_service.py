import os
import smtplib
from email.mime.text import MIMEText


def is_email_alert_enabled():
    return os.getenv("ALERT_EMAIL_ENABLED", "false").lower() == "true"


def send_email_alert(subject, body):
    """
    Sends an email alert using SMTP.
    Secrets must come from .env, not from source code.
    """
    if not is_email_alert_enabled():
        print("Email alert: disabled.")
        return False

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    alert_from = os.getenv("ALERT_FROM_EMAIL")
    alert_to = os.getenv("ALERT_TO_EMAIL")

    required_values = [
        smtp_host,
        smtp_username,
        smtp_password,
        alert_from,
        alert_to
    ]

    if not all(required_values):
        print("Email alert: missing SMTP configuration.")
        return False

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = alert_from
    message["To"] = alert_to

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(alert_from, [alert_to], message.as_string())

        print(f"Email alert sent to {alert_to}")
        return True

    except Exception as error:
        print(f"Email alert failed: {error}")
        return False
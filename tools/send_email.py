import os
import smtplib
from email.mime.text import MIMEText
# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def send_email_gmail(to, subject, body):
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_password = os.environ.get('GMAIL_PASSWORD')
    if not gmail_user or not gmail_password:
        raise RuntimeError("GMAIL_USER and GMAIL_PASSWORD environment variables must be set.")
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, [to], msg.as_string())

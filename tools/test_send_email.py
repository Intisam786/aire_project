from tools.send_email import send_email_gmail

if __name__ == "__main__":
    to = "ahmed88013786@gmail.com"  # Change to your test email if needed
    subject = "AIRE Test Email"
    body = "This is a test email sent from the AIRE project pipeline."
    try:
        send_email_gmail(to, subject, body)
        print("Test email sent successfully.")
    except Exception as e:
        print(f"Failed to send test email: {e}")

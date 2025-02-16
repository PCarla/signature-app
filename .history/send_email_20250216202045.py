import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
def send_email_with_attachment(to_email, subject, body, attachment_path):
    """
    Sends an email with an attachment using environment variables for credentials.
    """
    try:
        # Retrieve email credentials from environment variables
        email_user = os.getenv('EMAIL_USER')
        email_pass = os.getenv('EMAIL_PASS')
        # Check if environment variables are set
        if not email_user or not email_pass:
            print("Email credentials are not set in environment variables.")
            return False
        # Create email
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_user
        msg['To'] = to_email
        msg.set_content(body)
        # Add attachment
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
# Example usage
if __name__ == "__main__":
    to_email = "recipient@example.com"  # Replace with the recipient's email address
    subject = "Bestätigung der Müllabholung"
    body = "Bitte finden Sie die beigefügte Bestätigung der Müllabholung."
    attachment_path = "bestaetigung.pdf"  # Replace with the path to your PDF file
    # Send the email
    send_email_with_attachment(to_email, subject, body, attachment_path)

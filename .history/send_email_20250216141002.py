import smtplib
from email.message import EmailMessage
import os

def send_email_with_attachment(to_email, subject, body, attachment_path):
    """
    Sends an email with an attachment.
    """
    try:
        # Create email
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = 'carla.patzanovsky@gmail.com
        msg['To'] = to_email
        msg.set_content(body)

        # Add attachment
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # Send email
        with smtplib.SMTP_SSL('smtp.example.com', 465) as smtp:
            smtp.login('your_email@example.com', 'your_password')
            smtp.send_message(msg)

        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Example call
to_email = "carla,patzanovsky@gmail.com
subject = "Bestätigung der Müllabholung"
body = "Bitte finden Sie die beigefügte Bestätigung der Müllabholung."
attachment_path = "output/bestaetigung.pdf"

send_email_with_attachment(to_email, subject, body, attachment_path)

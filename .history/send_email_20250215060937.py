import smtplib
from email.message import EmailMessage

def sende_email(empfaenger_email, pdf_pfad):
    msg = EmailMessage()
    msg["Subject"] = "Bestätigung Müllabholung"
    msg["From"] = "muellservice@example.com"
    msg["To"] = empfaenger_email
    msg.set_content("Hier ist die Bestätigung Ihrer Müllabholung.")

    with open(pdf_pfad, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="bestätigung.pdf")

    with smtplib.SMTP_SSL("smtp.example.com", 465) as smtp:
        smtp.login("muellservice@example.com", "passwort")
        smtp.send_message(msg)

sende_email("kunde@example.com", "bestätigung.pdf")

import smtplib
from email.message import EmailMessage

def sende_email(empfaenger_email, pdf_pfad):
    msg = EmailMessage()
    msg["Subject"] = "Bestätigung Müllabholung"
    msg["From"] = "carla.patzanovsky@gmail.com"
    msg["To"] = empfaenger_email
    msg.set_content("Hier ist die Bestätigung Ihrer Müllabholung.")

    with open(pdf_pfad, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="output/bestaetigung.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("carla.patzanovsky@gmail.com", "Meine_App_PW")
        smtp.send_message(msg)

sende_email("carla.patzanovsky@gmail.com", "output/bestaetigung.pdf")





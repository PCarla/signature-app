   import os
   from dotenv import load_dotenv
   import smtplib
   from email.message import EmailMessage
   # Laden der .env-Datei
   load_dotenv()
   def sende_email(empfaenger_email, pdf_pfad):
       email_user = os.getenv("EMAIL_USER")
       email_pass = os.getenv("EMAIL_PASS")
       if not email_user or not email_pass:
           print("E-Mail-Zugangsdaten sind nicht gesetzt.")
           return
       msg = EmailMessage()
       msg["Subject"] = "Bestätigung Müllabholung"
       msg["From"] = email_user
       msg["To"] = empfaenger_email
       msg.set_content("Hier ist die Bestätigung Ihrer Müllabholung.")
       with open(pdf_pfad, "rb") as f:
           msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="bestaetigung.pdf")
       with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
           smtp.login(email_user, email_pass)
           smtp.send_message(msg)
   # Beispielaufruf
   sende_email("carla.patzanovsky@gmail.com", "output/bestaetigung.pdf")

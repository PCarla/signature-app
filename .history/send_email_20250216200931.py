import os
import smtplib
from email.message import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
import tempfile
from dotenv import load_dotenv
# Laden der .env-Datei
load_dotenv()
def validate_base64(data):
    """
    Validates that the string is properly base64-encoded.
    """
    try:
        if len(data) % 4:
            data += '=' * (4 - len(data) % 4)
        base64.b64decode(data, validate=True)
        return True
    except (base64.binascii.Error, ValueError) as e:
        print(f"Validation error: {e}")
        return False
def generate_pdf(adresse, tonnen_anzahl, datum, signature_base64, output_filename):
    """
    Erstellt ein PDF-Dokument mit den angegebenen Daten und einer Unterschrift.
    """
    try:
        # PDF erstellen
        c = canvas.Canvas(output_filename, pagesize=letter)
        c.drawString(100, 750, "Bestätigung der Müllabholung")
        c.drawString(100, 730, f"Adresse: {adresse}")
        c.drawString(100, 710, f"Anzahl Mülltonnen: {tonnen_anzahl}")
        c.drawString(100, 690, f"Abholdatum: {datum}")
        # Unterschrift dekodieren
        if "data:image/png;base64," in signature_base64:
            signature_data = signature_base64.replace("data:image/png;base64,", "")
        else:
            signature_data = signature_base64
        print("Signature data to decode:", signature_data[:30] + "...")  # Debugging line
        # Validate Base64 data
        if not validate_base64(signature_data):
            print("Ungültige Base64-Daten.")
            return False
        try:
            # Base64-Daten dekodieren
            signature_bytes = base64.b64decode(signature_data, validate=True)
            print(f"Successfully decoded base64 data. Length: {len(signature_bytes)} bytes.")
        except (base64.binascii.Error, ValueError) as e:
            print(f"Ungültige Base64-Daten: {e}")
            return False
        # Temporäre Datei erstellen
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(signature_bytes)
                temp_file_path = temp_file.name
                print(f"Temporary signature file created at: {temp_file_path}")
            # Unterschrift ins PDF einfügen
            c.drawImage(temp_file_path, 100, 600, width=200, height=100)
        finally:
            # Temporäre Datei löschen
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        # PDF speichern
        c.showPage()
        c.save()
        print(f"PDF erfolgreich erstellt: {output_filename}")
        return True
    except Exception as e:
        print(f"Fehler beim Erstellen des PDFs: {e}")
        return False
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
# Beispielaufruf
if __name__ == "__main__":
    adresse = "Musterstraße 123, 12345 Musterstadt"
    tonnen_anzahl = 3
    datum = "2023-10-10"
    # Base64-codierte Signatur (aus der vorherigen Konvertierung)
    signature_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA..."  # Ersetzen Sie dies durch Ihre Base64-Daten
    # Name der Ausgabedatei
    output_filename = "bestaetigung.pdf"
    # PDF erstellen
    if generate_pdf(adresse, tonnen_anzahl, datum, signature_base64, output_filename):
        # E-Mail senden
        to_email = "carla.patzanovsky@gmail.com"
        subject = "Bestätigung der Müllabholung"
        body = "Bitte finden Sie die beigefügte Bestätigung der Müllabholung."
        send_email_with_attachment(to_email, subject, body, output_filename)

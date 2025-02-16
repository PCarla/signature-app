from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
import os
import tempfile

def validate_base64(data):
    """
    Validates that the string is properly base64-encoded.
    """
    try:
        # If the input data is not a multiple of 4, add padding
        if len(data) % 4:
            data += '=' * (4 - len(data) % 4)
        
        # Decode to check if the data is valid base64
        base64.b64decode(data, validate=True)
        return True
    except (base64.binascii.Error, ValueError) as e:
        print(f"Validation error: {e}")
        return False

def generate_pdf(adresse, tonnen_anzahl, datum, signature_base64, output_filename):
    """
    Erstellt ein PDF-Dokument mit den angegebenen Daten und einer Unterschrift.
    :param adresse: Adresse, die im PDF angezeigt wird
    :param tonnen_anzahl: Anzahl der Mülltonnen
    :param datum: Datum der Abholung
    :param signature_base64: Base64-codierte Signatur
    :param output_filename: Name der Ausgabedatei (PDF)
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
        
        # Strip non-base64 characters
        signature_data = ''.join(filter(lambda x: x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=', signature_data))
        
        # Validate Base64 data
        if not validate_base64(signature_data):
            print(f"Ungültige Base64-Daten: {signature_data[:30]}...")
            return False
        
        try:
            # Base64-Daten validieren und dekodieren
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

# Beispielaufruf
adresse = "Musterstraße 123, 12345 Musterstadt"
tonnen_anzahl = 3
datum = "2023-10-10"
# Base64-codierte Signatur (aus der vorherigen Konvertierung)
signature_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA..."  # Ersetzen Sie dies durch Ihre Base64-Daten
# Name der Ausgabedatei
output_filename = "bestaetigung.pdf"
# PDF erstellen
generate_pdf(adresse, tonnen_anzahl, datum, signature_base64, output_filename)

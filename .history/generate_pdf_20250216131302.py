from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
import io
import os
def generate_pdf(adresse, tonnen_anzahl, datum, signature_base64, output_filename):
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
        try:
            signature_bytes = base64.b64decode(signature_data)
            signature_io = io.BytesIO(signature_bytes)
            # Unterschrift ins PDF einfügen
            c.drawImage(signature_io, 100, 600, width=200, height=100)
        except Exception as e:
            print(f"Fehler beim Dekodieren der Unterschrift: {e}")
            return False
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
signature_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA..."  # Ersetzen Sie dies durch Ihre Base64-Daten
output_filename = "bestaetigung.pdf"
generate_pdf(adresse, tonnen_anzahl, datum, signature_base64, output_filename)

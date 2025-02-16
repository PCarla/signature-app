from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
import io

def generate_pdf(adresse, tonnen_anzahl, datum, signature_base64, output_filename):
    c = canvas.Canvas(output_filename, pagesize=letter)
    c.drawString(100, 750, f"Bestätigung der Müllabholung")
    c.drawString(100, 730, f"Adresse: {adresse}")
    c.drawString(100, 710, f"Anzahl Mülltonnen: {tonnen_anzahl}")
    c.drawString(100, 690, f"Abholdatum: {datum}")

    # Unterschrift dekodieren
    signature_data = signature_base64.replace("data:image/png;base64,", "")
    signature_bytes = base64.b64decode(signature_data)
    signature_io = io.BytesIO(signature_bytes)
    
    c.drawImage(signature_io, 100, 600, width=200, height=100)
    c.showPage()
    c.save()

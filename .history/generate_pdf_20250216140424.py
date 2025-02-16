from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
import os
import tempfile

def decode_base64_image(base64_string):
    """
    Decodes a base64 string to bytes.
    """
    if "data:image/png;base64," in base64_string:
        base64_string = base64_string.replace("data:image/png;base64,", "")
    return base64.b64decode(base64_string)

def generate_pdf(adresse, tonnen_anzahl, datum, signature_base64, container_image_paths, output_filename):
    """
    Generates a PDF with the given data and images.
    """
    try:
        # Create PDF
        c = canvas.Canvas(output_filename, pagesize=letter)
        c.drawString(100, 750, "Bestätigung der Müllabholung")
        c.drawString(100, 730, f"Adresse: {adresse}")
        c.drawString(100, 710, f"Anzahl Mülltonnen: {tonnen_anzahl}")
        c.drawString(100, 690, f"Abholdatum: {datum}")

        # Decode and add signature image
        signature_bytes = decode_base64_image(signature_base64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(signature_bytes)
            signature_path = temp_file.name
        c.drawImage(signature_path, 100, 600, width=200, height=100)
        os.remove(signature_path)

        # Add container images
        y_position = 500
        for image_path in container_image_paths:
            c.drawImage(image_path, 100, y_position, width=200, height=150)
            y_position -= 200

        # Save PDF
        c.showPage()
        c.save()
        print(f"PDF erfolgreich erstellt: {output_filename}")
        return True
    except Exception as e:
        print(f"Fehler beim Erstellen des PDFs: {e}")
        return False

# Example call
adresse = "Musterstraße 123, 12345 Musterstadt"
tonnen_anzahl = 3
datum = "2023-10-10"
signature_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAEElEQVR42mP8z/CfAQAI" \
                   "AAL/3GvcywAAAABJRU5ErkJggg=="
container_image_paths = ["container1.png", "container2.png"]  # Add paths to container images
output_filename = "bestaetigung.pdf"

generate_pdf(adresse, tonnen_anzahl, datum, signature_base64, container_image_paths, output_filename)

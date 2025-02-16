from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(adresse, tonnen_anzahl, datum, signature_image, test_image, output_filename):
    """
    Generates a PDF with the given data and images.
    :param adresse: Address to be displayed in the PDF
    :param tonnen_anzahl: Number of bins
    :param datum: Date of collection
    :param signature_image: Path to the signature image
    :param test_image: Path to the test image
    :param output_filename: Name of the output PDF file
    """
    try:
        # Create PDF
        c = canvas.Canvas(output_filename, pagesize=letter)
        c.drawString(100, 750, "Bestätigung der Müllabholung")
        c.drawString(100, 730, f"Adresse: {adresse}")
        c.drawString(100, 710, f"Anzahl Mülltonnen: {tonnen_anzahl}")
        c.drawString(100, 690, f"Abholdatum: {datum}")

        # Add signature image
        if os.path.exists(signature_image):
            c.drawImage(signature_image, 100, 600, width=200, height=100)
        else:
            print(f"Signature image not found: {signature_image}")

        # Add test image
        if os.path.exists(test_image):
            c.drawImage(test_image, 100, 400, width=200, height=150)
        else:
            print(f"Test image not found: {test_image}")

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
signature_image = "signature.png"
test_image = "testbild.jpg"
output_filename = "output/bestaetigung.pdf"

if not os.path.exists("output"):
    os.makedirs("output")

generate_pdf(adresse, tonnen_anzahl, datum, signature_image, test_image, output_filename)

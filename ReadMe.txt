Super! Hier ist eine detaillierte Schritt-für-Schritt-Anleitung, um dein System zu bauen.
Das Ziel ist:
✅ Müllmann macht ein Foto von den Tonnen (PWA/Web-App)
✅ KI zählt die Tonnen automatisch (Google Vision API)
✅ Kunde unterschreibt auf einem Tablet (HTML5 Canvas)
✅ System generiert ein PDF mit allen Daten
✅ PDF wird automatisch per E-Mail versendet

🔹 1. Google Vision API für automatische Tonnenzählung
AIzaSyAmYQQkW3GpRgRlqEmNfgD1YM6R-zH6ulU
Zuerst richten wir die Google Vision API ein, damit das System automatisch die Anzahl der Mülltonnen auf dem Foto erkennt.

1️⃣ Google Cloud Vision API aktivieren
	1.	Gehe zur Google Cloud Console: Google Cloud Console
	2.	Neues Projekt erstellen (muellabholung-ai)
	3.	Vision API aktivieren:
	•	Gehe zu APIs & Services → Bibliothek
	•	Suche nach Cloud Vision API und aktiviere sie
	4.	Authentifizierung einrichten:
	•	Gehe zu APIs & Dienste → Anmeldedaten
	•	Erstelle einen neuen API-Schlüssel
	•	Lade die JSON-Datei (credentials.json) herunter und speichere sie im Projektordner

2️⃣ Python-Skript zum Zählen der Tonnen

Installiere zuerst das google-cloud-vision Paket:

pip install google-cloud-vision

Dann erstelle die Datei vision_api.py:

mport requests

API_KEY = "DEIN_API_SCHLÜSSEL"
IMAGE_PATH = "testbild.jpg"

def vision_api(image_path):
    with open(image_path, "rb") as img:
        img_data = img.read()

    response = requests.post(
        f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}",
        json={
            "requests": [
                {
                    "image": {"content": img_data.decode("latin1")},
                    "features": [{"type": "OBJECT_LOCALIZATION"}],
                }
            ]
        },
    )

    print(response.json())

vision_api(IMAGE_PATH)
********************************
from google.cloud import vision
import io

def zaehle_tonnen(image_path):
    """Zählt die Mülltonnen auf einem Bild mit der Google Vision API"""
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    tonnen_zaehler = sum(1 for obj in objects if "Trash bin" in obj.name)

    print(f"Erkannte Mülltonnen: {tonnen_zaehler}")
    return tonnen_zaehler

Testen:

export GOOGLE_APPLICATION_CREDENTIALS="credentials.json"
python vision_api.py

✅ Das Skript gibt die Anzahl der Mülltonnen auf dem Bild zurück.

🔹 2. Unterschrift des Kunden auf dem Tablet

Wir fügen eine digitale Unterschrift hinzu, die direkt im Browser auf einem Tablet oder Mobilgerät erfasst wird.

Erstelle die Datei signature.html:

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unterschrift erfassen</title>
    <style>
        canvas { border: 1px solid black; }
    </style>
</head>
<body>
    <h1>Bitte unterschreiben</h1>
    <canvas id="signature-pad" width="400" height="200"></canvas>
    <button onclick="clearSignature()">Löschen</button>
    <button onclick="saveSignature()">Speichern</button>

    <script>
        const canvas = document.getElementById("signature-pad");
        const ctx = canvas.getContext("2d");
        let drawing = false;

        canvas.addEventListener("mousedown", () => drawing = true);
        canvas.addEventListener("mouseup", () => drawing = false);
        canvas.addEventListener("mousemove", draw);

        function draw(event) {
            if (!drawing) return;
            ctx.lineTo(event.offsetX, event.offsetY);
            ctx.stroke();
        }

        function clearSignature() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }

        function saveSignature() {
            const dataURL = canvas.toDataURL();
            fetch("https://mein-backend.com/save_signature", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ signature: dataURL }),
            });
            alert("Unterschrift gespeichert!");
        }
    </script>
</body>
</html>

✅ Der Kunde kann direkt auf dem Tablet unterschreiben!

🔹 3. PDF-Generierung mit Unterschrift

Jetzt erstellen wir ein PDF, das die Tonnenzahl + Unterschrift enthält.

Installiere zuerst reportlab für PDF-Generierung:

pip install reportlab

Dann erstelle generate_pdf.py:

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

✅ Jetzt wird ein PDF mit der Unterschrift generiert.

🔹 4. Automatische E-Mail mit PDF versenden

Wir versenden das PDF automatisch per E-Mail.

Installiere smtplib und email:

pip install secure-smtplib

Dann erstelle send_email.py:

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

✅ Jetzt erhalten Müllmann & Kunde automatisch eine Bestätigung per E-Mail!

🚀 Fazit: Vollständiges System

✅ Foto aufnehmen → KI zählt Tonnen
✅ Kunde unterschreibt digital auf dem Tablet
✅ PDF wird mit Daten & Unterschrift erstellt
✅ E-Mail wird automatisch mit PDF gesendet

Was als nächstes?
	•	Soll die App auch mit PWA kombiniert werden?
	•	Soll es eine Admin-Oberfläche geben, um alte Bestätigungen einzusehen?



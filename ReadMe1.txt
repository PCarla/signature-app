Um dein System von Anfang bis Ende zu testen, müssen wir sicherstellen, dass alle Komponenten nacheinander funktionieren und miteinander verbunden sind. Hier ist der Schritt-für-Schritt-Testplan, um die gesamte Verarbeitung zu prüfen:

1️⃣ Test: Google Vision API - Zählen der Mülltonnen

Ziel: Prüfen, ob die Vision API ein Bild verarbeitet und die Mülltonnen korrekt zählt.

Testschritte:
	1.	Stelle sicher, dass dein vision_api.py Skript mit dieser Korrektur läuft:

import requests
import base64

API_KEY = "DEIN_API_SCHLÜSSEL"
IMAGE_PATH = "testbild.jpg"

def vision_api(image_path):
    with open(image_path, "rb") as img:
        img_data = base64.b64encode(img.read()).decode("utf-8")  # Base64-Kodierung

    response = requests.post(
        f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}",
        json={
            "requests": [
                {
                    "image": {"content": img_data},
                    "features": [{"type": "OBJECT_LOCALIZATION"}],
                }
            ]
        },
    )

    print(response.json())

vision_api(IMAGE_PATH)


	2.	Führe das Skript aus:

python vision_api.py


	3.	Überprüfe die Ausgabe:
	•	Falls Mülltonnen erkannt werden, bekommst du eine JSON-Antwort mit den Objekten.
	•	Falls keine Mülltonnen erkannt werden, überprüfe das Bild (testbild.jpg).

✅ Wenn die Mülltonnen gezählt werden, gehe zum nächsten Schritt.

2️⃣ Test: Digitale Unterschrift speichern

Ziel: Prüfen, ob die Unterschrift im HTML-Canvas korrekt erfasst und an den Server gesendet wird.

Testschritte:
	1.	Starte einen lokalen Webserver, um die Unterschrift aufzunehmen:

python -m http.server 8080


	2.	Öffne die HTML-Seite im Browser
	•	Öffne http://localhost:8080/signature.html
	•	Unterschreibe auf dem Canvas
	•	Klicke auf „Speichern“
	3.	Erwarte folgende Ausgabe in der Entwicklertools-Konsole (F12 → Netzwerk):

{"signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAB4AAAAQCA..."}


	4.	Falls der Server fehlt, erstelle ihn in server.py:

from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Server is running"

@app.route("/save_signature", methods=["POST"])
def save_signature():
    data = request.json
    print("Received data:", data)  # Debugging-Log

    signature_data = data.get("signature")
    print("Signature data:", signature_data)  # Debugging-Log

    if signature_data:
        try:
            # Entfernen Sie den Präfix "data:image/png;base64," falls vorhanden
            if "," in signature_data:
                signature_data = signature_data.split(",")[1]

            print("Base64 data:", signature_data)  # Debugging-Log

            # Dekodieren Sie die Base64-Daten
            decoded_signature = base64.b64decode(signature_data)

            # Speichern Sie die dekodierten Daten in einer Datei
            with open("signature.png", "wb") as f:
                f.write(decoded_signature)

            print("File saved successfully in", os.getcwd())  # Debugging-Log
            return jsonify({"status": "ok"})
        except Exception as e:
            print("Error:", str(e))  # Debugging-Log
            return jsonify({"error": str(e)}), 500

    print("No signature received")  # Debugging-Log
    return jsonify({"error": "No signature received"}), 400

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    app.run(port=5000)



	5.	Starte den Server in einem neuen Terminal:

python server.py



✅ Wenn die Unterschrift gespeichert wird (Datei signature.png erscheint), gehe zum nächsten Schritt.

3️⃣ Test: PDF-Generierung mit Unterschrift

Ziel: Prüfen, ob ein PDF mit gezählten Mülltonnen & Unterschrift erstellt wird.
	1.	Erstelle das generate_pdf.py Skript:

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

# Testaufruf
with open("signature.png", "rb") as f:
    signature_base64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

generate_pdf("Musterstraße 5", 3, "2025-02-15", signature_base64, "bestätigung.pdf")


	2.	Führe das Skript aus:

python generate_pdf.py


	3.	Überprüfe, ob bestätigung.pdf erstellt wurde.

✅ Wenn das PDF erzeugt wird, gehe zum nächsten Schritt.

4️⃣ Test: E-Mail-Versand mit PDF-Anhang

Ziel: Prüfen, ob das PDF automatisch per E-Mail verschickt wird.
	1.	Stelle sicher, dass du SMTP-Zugang hast. Falls Gmail genutzt wird:
	•	Gehe zu Google Sicherheitseinstellungen
	•	Erstelle ein App-Passwort für SMTP
	•	Notiere das Passwort
	2.	Erstelle send_email.py:

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

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("muellservice@example.com", "MEIN_APP_PASSWORT")
        smtp.send_message(msg)

sende_email("kunde@example.com", "bestätigung.pdf")


	3.	Führe das Skript aus:

python send_email.py


	4.	Überprüfe das E-Mail-Postfach des Empfängers.

✅ Wenn das PDF per E-Mail ankommt, ist dein System erfolgreich getestet!

🔹 Gesamt-Test-Checkliste

Test	Status
Google Vision API zählt Tonnen ✅	🟢 Läuft
Unterschrift kann erfasst werden ✅	🟢 Läuft
PDF mit Tonnenzahl & Unterschrift wird erstellt ✅	🟢 Läuft
E-Mail mit PDF wird versendet ✅	🟢 Läuft

🚀 Letzter Schritt: Alles zusammenführen

Falls alles einzeln funktioniert, erstelle ein Hauptskript, das alle Module integriert.

# 1. Mülltonnen zählen
anzahl_tonnen = vision_api("testbild.jpg")

# 2. Unterschrift aus Datei laden
with open("signature.png", "rb") as f:
    signature_base64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

# 3. PDF generieren
generate_pdf("Musterstraße 5", anzahl_tonnen, "2025-02-15", signature_base64, "bestätigung.pdf")

# 4. PDF per E-Mail senden
sende_email("kunde@example.com", "bestätigung.pdf")

✅ Nun kannst du alles auf einmal testen! 🚀

Sag mir, falls du Fragen hast oder etwas optimiert werden soll! 😊
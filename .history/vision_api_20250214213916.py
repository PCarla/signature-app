import base64
import requests
import io
import json


API_KEY = "AIzaSyAmYQQkW3GpRgRlqEmNfgD1YM6R-zH6ulU"
IMAGE_PATH = "testbild.jpg"



def zaehle_tonnen(image_path, api_key):
    """Zählt die Mülltonnen auf einem Bild mit der Google Vision API."""
    # Lese den Bildinhalt
    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    # Codiert den Bildinhalt in Base64
    img_data = base64.b64encode(content).decode("utf-8")

    # Erstelle die Anfrage an die Google Vision API
    response = requests.post(
        f"https://vision.googleapis.com/v1/images:annotate?key={api_key}",
        json={
            "requests": [
                {
                    "image": {"content": img_data},
                    "features": [{"type": "OBJECT_LOCALIZATION"}],
                }
            ]
        },
    )

    # Überprüfe auf Fehler in der API-Antwort
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")

    response_data = response.json()

    # Gebe die vollständige API-Antwort aus (für Debugging-Zwecke)
    print(json.dumps(response_data, indent=2))

    # Extrahiere die erkannten Objekte
    objects = response_data["responses"][0].get("localizedObjectAnnotations", [])

    # Zähle die erkannten Mülltonnen
    tonnen_zaehler = sum(1 for obj in objects if "Trash bin" in obj["name"])

    # Ausgabe der Anzahl der erkannten Mülltonnen
    print(f"Erkannte Mülltonnen: {tonnen_zaehler}")
    return tonnen_zaehler

# Beispielaufruf der Funktion
# Ersetze 'your_api_key' und 'your_image.jpg' mit den tatsächlichen Werten
api_key = 'your_api_key'
image_path = 'path_to_your_image.jpg'
zaehle_tonnen(image_path, api_key)

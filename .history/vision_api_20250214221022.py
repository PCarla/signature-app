import base64
import requests
import io
import json


api_key = "AIzaSyAmYQQkW3GpRgRlqEmNfgD1YM6R-zH6ulU"
image_path = "testbild1.jpg"





def zaehle_tonnen(image_path, api_key):
    """Zählt die Mülltonnen auf einem Bild mit der Google Vision API und gibt detaillierte Informationen aus."""
    # Überprüfe, ob die Bilddatei existiert
    try:
        with io.open(image_path, "rb") as image_file:
            content = image_file.read()
    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden - {image_path}")
        return

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

    # Liste möglicher Begriffe für Mülltonnen (kann erweitert werden)
    muelltonnen_begriffe = ["Trash bin", "Garbage bin", "Waste container"]

    # Zähle die erkannten Mülltonnen und sammle detaillierte Informationen
    tonnen_info = []
    for obj in objects:
        if any(term in obj["name"] for term in muelltonnen_begriffe):
            info = {
                "name": obj["name"],
                "score": obj["score"],
                "boundingPoly": obj["boundingPoly"]["normalizedVertices"]
            }
            tonnen_info.append(info)
    
    tonnen_zaehler = len(tonnen_info)

    # Ausgabe der Anzahl der erkannten Mülltonnen
    print(f"Erkannte Mülltonnen: {tonnen_zaehler}")

    # Ausgabe der detaillierten Informationen zu den erkannten Mülltonnen
    for idx, info in enumerate(tonnen_info):
        print(f"Tonne {idx + 1}:")
        print(f"  Name: {info['name']}")
        print(f"  Erkennungsscore: {info['score']:.2f}")
        print("  Position (normalized bounding box):")
        for vertex in info["boundingPoly"]:
            print(f"    - ({vertex['x']:.2f}, {vertex['y']:.2f})")

    return tonnen_zaehler

# Beispielaufruf der Funktion
# Ersetze 'your_api_key' und 'your_image.jpg' mit den tatsächlichen Werten

zaehle_tonnen(image_path, api_key)


#AIzaSyAmYQQkW3GpRgRlqEmNfgD1YM6R-zH6ulU
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
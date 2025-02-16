import requests
import base64

API_KEY = "AIzaSyAmYQQkW3GpRgRlqEmNfgD1YM6R-zH6ulU"
IMAGE_PATH = "testbild.jpg"

def vision_api(image_path, api_key):
    try:
        with open(image_path, "rb") as img:
            img_data = base64.b64encode(img.read()).decode("utf-8")  # Base64-Kodierung

        response = requests.post(
            f"https://vision.googleapis.com/v1/images:annotate?key={api_key}",
            json={
                "requests": [
                    {
                        "image": {"content": img_data},
                        "features": [
                            {"type": "LABEL_DETECTION"},
                            {"type": "OBJECT_LOCALIZATION"}
                        ],
                    }
                ]
            },
        )

        if response.status_code == 200:
            parse_response(response.json())
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except FileNotFoundError:
        print(f"Error: the file {image_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def parse_response(response):
    for resp in response['responses']:
        if 'labelAnnotations' in resp:
            print("Erkannte Labels:")
            for label in resp['labelAnnotations']:
                print(f"Label: {label['description']}, Score: {label['score']}")

        if 'localizedObjectAnnotations' in resp:
            print("\nErkannte Objekte (mit Bounding-Boxen):")
            for obj in resp['localizedObjectAnnotations']:
                name = obj['name']
                score = obj['score']
                vertices = obj['boundingPoly']['normalizedVertices']
                
                # Berechnung der Bounding-Box-Größe
                width = vertices[2]['x'] - vertices[0]['x']
                height = vertices[2]['y'] - vertices[0]['y']
                area = width * height
                
                print(f"Name: {name}, Score: {score}")
                print(f"Bounding Box: {vertices}")
                print(f"Width: {width}, Height: {height}, Area: {area}\n")
# Beispielaufruf

vision_api(IMAGE_PATH, API_KEY)

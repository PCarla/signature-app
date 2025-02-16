import requests
import base64

API_KEY = "AIzaSyAmYQQkW3GpRgRlqEmNfgD1YM6R-zH6ulU"
IMAGE_PATH = "testbild.jpg"

ddef vision_api(image_path, api_key):
    try:
        with open(image_path, "rb") as img:
            img_data = base64.b64encode(img.read()).decode("utf-8")  # Base64-Kodierung

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

        if response.status_code == 200:
            parse_response(response.json())
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except FileNotFoundError:
        print(f"Error: the file {image_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def parse_response(response):
    # Gehe durch jede Antwort im Response
    for resp in response['responses']:
        if 'localizedObjectAnnotations' in resp:
            print("Erkannte Objekte:")
            for obj in resp['localizedObjectAnnotations']:
                print(f"Name: {obj['name']}, Score: {obj['score']}")

# Beispielaufruf

vision_api(IMAGE_PATH)

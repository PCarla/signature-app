import requests
import base64

API_KEY = "AIzaSyAmYQQkW3GpRgRlqEmNfgD1YM6R-zH6ulU"
IMAGE_PATH = "testbild.jpg"

def vision_api(image_path):
    try:
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

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except FileNotFoundError:
        print(f"Error: the file {image_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Beispielaufruf

vision_api(IMAGE_PATH)

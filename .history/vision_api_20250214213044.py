mport requests
import base64

API_KEY = "AIzaSyAmYQQkW3GpRgRlqEmNfgD1YM6R-zH6ulU"
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
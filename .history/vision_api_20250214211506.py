import requests

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
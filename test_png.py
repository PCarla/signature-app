import base64
def convert_png_to_base64(png_file_path):
    """
    Konvertiert eine PNG-Datei in einen Base64-codierten String.
    :param png_file_path: Pfad zur PNG-Datei
    :return: Base64-codierter String mit Präfix
    """
    try:
        # Öffnen der PNG-Datei im Binärmodus
        with open(png_file_path, "rb") as f:
            # Lesen der Datei und Konvertieren in Base64
            signature_base64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
        return signature_base64
    except FileNotFoundError:
        print(f"Die Datei '{png_file_path}' wurde nicht gefunden.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None
if __name__ == "__main__":
    # Pfad zur PNG-Datei
    png_file_path = "signature.png"
    # Konvertieren der PNG-Datei in Base64
    signature_base64 = convert_png_to_base64(png_file_path)
    if signature_base64:
        # Ausgabe des Base64-codierten Strings
        print("Base64-codierte Signatur:")
        print(signature_base64)

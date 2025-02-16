from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Server is running"

@app.route("/save_signature", methods=["POST"])
def save_signature():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging-Log

        if not data:
            print("No data received")  # Debugging-Log
            return jsonify({"error": "No data received"}), 400

        signature_data = data.get("signature")
        print("Signature data:", signature_data)  # Debugging-Log

        if not signature_data:
            print("No signature received")  # Debugging-Log
            return jsonify({"error": "No signature received"}), 400

        # Entfernen Sie den Präfix "data:image/png;base64," falls vorhanden
        if signature_data.startswith("data:image/png;base64,"):
            signature_data = signature_data.split(",")[1]

        print("Base64 data before padding correction:", signature_data[:30] + "...")  # Debugging-Log

        # Korrigieren Sie das Padding, falls nötig
        missing_padding = len(signature_data) % 4
        if missing_padding:
            signature_data += '=' * (4 - missing_padding)

        print("Base64 data after padding correction:", signature_data[:30] + "...")  # Debugging-Log

        # Dekodieren Sie die Base64-Daten
        decoded_signature = base64.b64decode(signature_data)
        print("Decoded signature length:", len(decoded_signature))  # Debugging-Log

        # Überprüfen Sie die ersten paar Bytes, um sicherzustellen, dass es sich um ein PNG-Bild handelt
        if decoded_signature[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError("Decoded data is not a valid PNG file")

        # Speichern Sie die dekodierten Daten in einer Datei
        with open("signature.png", "wb") as f:
            f.write(decoded_signature)

        print("File saved successfully in", os.getcwd())  # Debugging-Log
        return jsonify({"status": "ok"})

    except Exception as e:
        print("Error:", str(e))  # Debugging-Log
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    app.run(port=5000)

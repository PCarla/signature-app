from flask import Flask, request, jsonify
import base64
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Server is running"

@app.route("/save_signature", methods=["POST"])
def save_signature():
    data = request.json
    print("Received data:", data)  # Debugging-Log

    signature_data = data.get("signature")
    print("Signature data:", signature_data)  # Debugging-Log

    if signature_data:
        try:
            # Entfernen Sie den Präfix "data:image/png;base64," falls vorhanden
            if "," in signature_data:
                signature_data = signature_data.split(",")[1]

            print("Base64 data:", signature_data)  # Debugging-Log

            # Dekodieren Sie die Base64-Daten
            decoded_signature = base64.b64decode(signature_data)

            # Speichern Sie die dekodierten Daten in einer Datei
            with open("signature.png", "wb") as f:
                f.write(decoded_signature)

            print("File saved successfully in", os.getcwd())  # Debugging-Log
            return jsonify({"status": "ok"})
        except Exception as e:
            print("Error:", str(e))  # Debugging-Log
            return jsonify({"error": str(e)}), 500

    print("No signature received")  # Debugging-Log
    return jsonify({"error": "No signature received"}), 400

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    app.run(host='127.0.0.1', port=5000,debug=True)

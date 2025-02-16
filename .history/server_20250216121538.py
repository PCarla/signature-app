from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/save_signature", methods=["POST"])
def save_signature():
    data = request.json
    signature_data = data.get("signature")

    if signature_data:
        try:
            # Entfernen Sie den Präfix "data:image/png;base64," falls vorhanden
            if "," in signature_data:
                signature_data = signature_data.split(",")[1]

            # Dekodieren Sie die Base64-Daten
            import base64
            decoded_signature = base64.b64decode(signature_data)

            # Speichern Sie die dekodierten Daten in einer Datei
            with open("signature.png", "wb") as f:
                f.write(decoded_signature)

            return jsonify({"status": "ok"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "No signature received"}), 400

if __name__ == "__main__":
    app.run(port=5000)

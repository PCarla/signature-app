from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import base64


app = Flask(__name__)
CORS(app)


# Endpunkt für die HTML-Datei

@app.route("/signature.html")
def serve_signature():
    return send_from_directory(".", "signature.html")















# Endpunkt für das Speichern der Signatur





@app.route("/save_signature", methods=["POST"])
def save_signature():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400
        signature_data = data.get("signature")
        if not signature_data:
            return jsonify({"error": "No signature received"}), 400
        if "," not in signature_data:
            return jsonify({"error": "Invalid signature format"}), 400
        base64_data = signature_data.split(",")[1]
        with open("signature.png", "wb") as f:
            f.write(base64.b64decode(base64_data))
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred: {}".format(str(e))
        }), 500


if __name__ == "__main__":
    app.run(port=8080)

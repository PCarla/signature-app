from flask import Flask, request, jsonify, send_from_directory
import base64
import os
from flask_cors import CORS
import logging
def create_app():
    app = Flask(__name__)
    # Konfigurieren Sie CORS, um nur bestimmte Domains zuzulassen
    CORS(app, resources={r"/*": {"origins": "*"}})
    # Logging konfigurieren
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    @app.route("/")
    def index():
        return "Server is running"
    @app.route("/signature")
    def serve_signature_html():
        try:
            return send_from_directory("static", "signature.html")
        except FileNotFoundError:
            logger.error("signature.html not found in the static directory.")
            return jsonify({"error": "signature.html not found"}), 404
    @app.route("/save_signature", methods=["POST"])
    def save_signature():
        data = request.json
        if not data:
            logger.error("No JSON payload received.")
            return jsonify({"error": "No JSON payload received"}), 400
        signature_data = data.get("signature")
        if not signature_data:
            logger.error("No signature received in the request.")
            return jsonify({"error": "No signature received"}), 400
        try:
            # Entfernen Sie den Präfix "data:image/png;base64," falls vorhanden
            if "," in signature_data:
                signature_data = signature_data.split(",")[1]
            # Base64-Daten dekodieren
            decoded_signature = base64.b64decode(signature_data)
            # Speichern der Signatur in einer Datei
            signature_path = os.path.join("static", "signature.png")
            with open(signature_path, "wb") as f:
                f.write(decoded_signature)
            logger.info(f"Signature saved successfully at {signature_path}")
            return jsonify({"status": "ok"})
        except base64.binascii.Error as e:
            logger.error(f"Invalid Base64 data: {e}")
            return jsonify({"error": "Invalid Base64 data"}), 400
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return jsonify({"error": str(e)}), 500
    return app
app = create_app()
if __name__ == "__main__":
    print("Starting Flask server...")
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)


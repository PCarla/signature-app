from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen
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
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
if __name__ == "__main__":
    app.run(port=5000)

from flask import Flask, request, jsonify, send_from_directory
import base64
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    @app.route("/")
    def index():
        return "Server is running"
    
    @app.route("/signature")
    def serve_signature_html():
        return send_from_directory("static", "signature.html")
    
    @app.route("/save_signature", methods=["POST"])
    def save_signature():
        data = request.json
        signature_data = data.get("signature")
        if signature_data:
            try:
                if "," in signature_data:
                    signature_data = signature_data.split(",")[1]
                decoded_signature = base64.b64decode(signature_data)
                with open("signature.png", "wb") as f:
                    f.write(decoded_signature)
                return jsonify({"status": "ok"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        return jsonify({"error": "No signature received"}), 400
    
    return app


app = create_app()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import base64


app = Flask(__name__)
CORS(app)


# Endpunkt für die HTML-Datei

@app.route("/signature.html")
def serve_signature():


# Endpunkt für das Speichern der Signatur

@app.route("/save_signature", methods=["POST"])
def save_signature():


if __name__ == "__main__":

    app.run(port=8080)

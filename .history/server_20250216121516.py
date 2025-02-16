from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/save_signature", methods=["POST"])
def save_signature():
    data = request.json
    signature_data = data.get("signature")

    if signature_data:
        with open("signature.png", "wb") as f:
            import base64
            f.write(base64.b64decode(signature_data.split(",")[1]))

        return jsonify({"status": "ok"})
    return jsonify({"error": "No signature received"}), 400

if __name__ == "_main_":
    app.run(port=5000)

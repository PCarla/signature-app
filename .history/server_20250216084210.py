from flask import Flask, request, jsonify
import base64
import os


app = Flask(__name__, static_folder=os.getcwd())


@app.route("/")
def index():
    return "Server is running"


@app.route("/signature")
def serve_signature():
    return app.send_static_file("signature.html")


@app.route("/save_signature", methods=["POST"])
def save_signature():
    data = request.json
    print("Received data:", data)

    if not data:
        print("No data received")
        return jsonify({"error": "No data received"}), 400

    signature_data = data.get("signature")
    print("Signature data:", signature_data)

    if not signature_data:
        print("No signature received")
        return jsonify({"error": "No signature received""), 400

    try:
        # Remove prefix if present
        if "," in signature_data:
            signature_data = signature_data.split(",")[1]

        print("Base64 data before padding correction:",
              signature_data[:30] + "...")

        # Fix padding if needed
        missing_padding = len(signature_data) % 4
        if missing_padding:
            signature_data += '=' * (4 - missing_padding)

        print("Base64 data after padding correction:",
              signature_data[:30] + "...")

        # Decode base64 data
        decoded_signature = base64.b64decode(signature_data)
        print("Decoded signature length:", len(decoded_signature))

        # Validate PNG file
        if decoded_signature[:8] == b'\x89PNG\r\n\x1a\n':
            print("Valid PNG file detected")

            # Save decoded data
            with open("signature.png", "wb") as f:
                f.write(decoded_signature)

            print("File saved successfully in", os.getcwd())
            return jsonify({"status": "ok"})
        else:
            print("Decoded data is not a PNG file")
            return jsonify({"error": "Decoded data is not a valid PNG file"}), 400

    except Exception as e:
        print("Base64 decoding error:", str(e))
        error_data = {
            "error": "Base64 decoding error",
            "details": str(e)
        }
        return jsonify(error_data), 500


if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    print("Static files directory:", app.static_folder)
    app.run(port=5000)

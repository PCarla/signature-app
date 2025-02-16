from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Server is running"

@app.route("/save_signature", methods=["POST"])
def save_signature():
    # Verify content type
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No JSON data received"}), 400

        signature_data = data.get("signature")
        if not signature_data:
            return jsonify({"error": "Missing 'signature' in request"}), 400

        # Remove the prefix "data:image/png;base64," if present
        if signature_data.startswith("data:image/png;base64,"):
            signature_data = signature_data.split(",")[1]

        # Correct padding if necessary
        missing_padding = len(signature_data) % 4
        if missing_padding:
            signature_data += '=' * (4 - missing_padding)

        # Decode the Base64 data
        decoded_signature = base64.b64decode(signature_data)

        # Check the first few bytes to ensure it's a PNG file
        if decoded_signature[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError("Decoded data is not a valid PNG file")

        # Save the decoded data to a file
        file_path = os.path.join(os.getcwd(), "signature.png")
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
        with open(file_path, "wb") as f:
            f.write(decoded_signature)
        os.chmod(file_path, 0o644)
            
        return jsonify({"status": "ok", "file_path": file_path})

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    app.static_folder = os.getcwd()
    app.run(port=5000)

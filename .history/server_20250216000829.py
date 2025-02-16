from flask import Flask, request, jsonify
import base64
import os


app = Flask(__name__)


@app.route("/")
def index():
    return "Server is running"


@app.route("/signature")
def serve_signature():
    return app.send_static_file("signature.html")


@app.route("/save_signature", methods=["POST"])
def save_signature():
    # Verify content type
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No JSON data received"}), 400

        print("Received data type:", type(data))
        print("Received data keys:", data.keys() if data else "No data")

        signature_data = data.get("signature")
        if not signature_data:
            return jsonify({"error": "Missing 'signature' in request"}), 400
            
        print("Signature data type:", type(signature_data))
        print("Signature data length:", len(signature_data) if signature_data else 0)

        # Remove the prefix "data:image/png;base64," if present
        if signature_data.startswith("data:image/png;base64,"):
            signature_data = signature_data.split(",")[1]

        print("Base64 data before padding correction:", 
              signature_data[:30] + "...")

        # Correct padding if necessary
        missing_padding = len(signature_data) % 4
        if missing_padding:
            signature_data += '=' * (4 - missing_padding)

        print("Base64 data after padding correction:", 
              signature_data[:30] + "...")

        # Decode the Base64 data
        decoded_signature = base64.b64decode(signature_data)
        print("Decoded signature length:", len(decoded_signature))

        # Check the first few bytes to ensure it's a PNG file
        if decoded_signature[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError("Decoded data is not a valid PNG file")

        # Save the decoded data to a file
        try:
            file_path = os.path.join(os.getcwd(), "signature.png")
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            print("Attempting to save to:", file_path)
            print("Current working directory:", os.getcwd())
            print("Full file path:", os.path.abspath(file_path))
            
            # Write file with explicit permissions
            with open(file_path, "wb") as f:
                f.write(decoded_signature)
            os.chmod(file_path, 0o644)
            
            print("File saved successfully")
            
            # Verify file was written
            if os.path.exists(file_path):
                print("File verification: exists, size:", 
                      os.path.getsize(file_path), "bytes")
                print("File permissions:", 
                      oct(os.stat(file_path).st_mode)[-3:])
                return jsonify({"status": "ok", "file_path": file_path})
            else:
                print("File verification failed: file does not exist")
                print("Directory contents:", os.listdir(os.getcwd()))
                return jsonify({
                    "error": "File could not be saved",
                    "directory": os.getcwd(),
                    "contents": os.listdir(os.getcwd())
                }), 500

        except IOError as e:
            print("File write error:", str(e))
            return jsonify({"error": f"File write error: {str(e)}"}), 500

    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    app.static_folder = os.getcwd()
    app.run(port=5000)

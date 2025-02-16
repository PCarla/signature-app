from flask import Flask, request, jsonify
import base64
import os


app = Flask(__name__)


@app.route("/")
def index():
    return "Server is running"


@app.route("/save_signature", methods=["POST"])
def save_signature():
    try:
        data = request.get_json()
        print("Received data type:", type(data))  # Debugging
        print("Received data keys:", 
              data.keys() if data else "No data")  # Debugging

        if not data:
            print("No data received in request body")  # Debugging
            return jsonify(
                {"error": "No JSON data received in request body"}), 400

        signature_data = data.get("signature")
        print("Signature data type:", type(signature_data))  # Debugging
        print("Signature data length:", 
              len(signature_data) if signature_data else 0)  # Debugging

        if not signature_data:
            print("No signature received")  # Debugging
            return jsonify({"error": "No signature received"}), 400

        # Remove the prefix "data:image/png;base64," if present
        if signature_data.startswith("data:image/png;base64,"):
            signature_data = signature_data.split(",")[1]

        print("Base64 data before padding correction:", 
              signature_data[:30] + "...")  # Debugging

        # Correct padding if necessary
        missing_padding = len(signature_data) % 4
        if missing_padding:
            signature_data += '=' * (4 - missing_padding)

        print("Base64 data after padding correction:", 
              signature_data[:30] + "...")  # Debugging

        # Decode the Base64 data
        decoded_signature = base64.b64decode(signature_data)
        print("Decoded signature length:", 
              len(decoded_signature))  # Debugging

        # Check the first few bytes to ensure it's a PNG file
        if decoded_signature[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError("Decoded data is not a valid PNG file")

        # Save the decoded data to a file
        try:
            file_path = os.path.join(os.getcwd(), "signature.png")
            print("Attempting to save to:", file_path)  # Debugging
            with open(file_path, "wb") as f:
                f.write(decoded_signature)
            print("File saved successfully")  # Debugging
            # Verify file was written
            if os.path.exists(file_path):
                print(
                    "File verification: exists, size:",
                    os.path.getsize(file_path),
                    "bytes"
                )  # Debugging
            else:
                print("File verification failed: file missing")  # Debugging


                return jsonify({"error": "File could not be saved"}), 500
        except IOError as e:
            print("File write error:", str(e))  # Debugging
            return jsonify({"error": f"File write error: {str(e)}"}), 500

        print("File saved successfully in", os.getcwd())  # Debugging
        return jsonify({"status": "ok"})

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    app.run(port=5000)

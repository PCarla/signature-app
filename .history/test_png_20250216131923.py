with open("signature.png", "rb") as f:
         signature_base64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

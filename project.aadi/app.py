from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
@app.route('/')
def home():
    return render_template("index.html")
CORS(app)  # This connects Frontend and Backend

@app.route('/scan', methods=['POST'])
def scan_website():
    data = request.json
    target_url = data.get('url')

    if not target_url:
        return jsonify({"status": "error", "message": "No URL provided"})

    if not target_url.startswith('http'):
        target_url = 'https://' + target_url

    try:
        response = requests.get(target_url, timeout=10)
        headers = response.headers

        results = {
            "A05: Security Misconfiguration": {
                "X-Frame-Options": "Safe" if "X-Frame-Options" in headers else "Missing (Risk: Clickjacking)",
                "X-Content-Type-Options": "Safe" if "X-Content-Type-Options" in headers else "Missing (Risk: MIME Sniffing)",
                "Content-Security-Policy": "Safe" if "Content-Security-Policy" in headers else "Missing (Risk: XSS)"
            },
            "Server_Info": headers.get('Server', 'Not Disclosed')
        }

        return jsonify({"status": "success", "data": results})

    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
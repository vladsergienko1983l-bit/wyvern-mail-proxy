from flask import Flask, jsonify, Response
import os
import requests
from mailru_cloud_guest_api import FileStreamGenerator

app = Flask(__name__)
PUBLIC_FILE = "https://cloud.mail.ru/public/Wiya/keZEiKNXe"
BASE_URL = os.getenv("BASE_URL", "https://wyvern-mail-proxy.onrender.com")

@app.get("/")
def health():
    return jsonify({"status": "ok", "service": "wyvern-mail-proxy"})

@app.get("/manifest.json")
def manifest():
    return jsonify({"version": "1.0.0", "clientUrl": BASE_URL + "/download/client"})

@app.get("/download/client")
def download_client():
    stream = FileStreamGenerator.of(PUBLIC_FILE).generate()
    upstream = requests.get(stream.stream_link, stream=True, timeout=120)
    upstream.raise_for_status()
    headers = {"Content-Type": upstream.headers.get("Content-Type", "application/octet-stream")}
    if upstream.headers.get("Content-Length"):
        headers["Content-Length"] = upstream.headers["Content-Length"]
    return Response(upstream.iter_content(chunk_size=1024 * 1024), headers=headers, direct_passthrough=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))

from flask import Flask, jsonify, redirect
import os
from mailru_cloud_guest_api import FileStreamGenerator

app = Flask(__name__)
PUBLIC_FILE = "https://cloud.mail.ru/public/Wiya/keZEiKNXe"

@app.get("/")
def health():
    return jsonify({"status": "ok", "service": "wyvern-mail-proxy"})

@app.get("/manifest.json")
def manifest():
    stream = FileStreamGenerator.of(PUBLIC_FILE).generate()
    return jsonify({"version": "1.0.0", "clientUrl": stream.stream_link})

@app.get("/download/client")
def download_client():
    stream = FileStreamGenerator.of(PUBLIC_FILE).generate()
    return redirect(stream.stream_link)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))

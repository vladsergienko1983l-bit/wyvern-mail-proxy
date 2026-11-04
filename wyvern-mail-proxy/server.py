from flask import Flask, jsonify
import os

app = Flask(__name__)

FILES = {
    "client": "https://cloud.mail.ru/public/Wiya/keZEiKNXe"
}

@app.get("/")
def health():
    return jsonify({"status": "ok", "service": "wyvern-mail-proxy"})

@app.get("/manifest.json")
def manifest():
    return jsonify({
        "version": "1.0.0",
        "clientUrl": FILES["client"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))

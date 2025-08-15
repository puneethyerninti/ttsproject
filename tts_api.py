# tts_api.py
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import os, io, zipfile, hashlib

app = Flask(__name__)
CORS(app)  # allow calls from frontend dev servers
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def tts_to_cached_mp3(text: str, lang: str = "en", slow: bool = False) -> str:
    """
    Convert text to speech and cache the mp3 by hash so repeated texts are instant.
    Returns the file path to the mp3.
    """
    key = hashlib.sha1(f"{lang}|{int(slow)}|{text}".encode("utf-8")).hexdigest()
    path = os.path.join(CACHE_DIR, f"{key}.mp3")
    if not os.path.exists(path):
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(path)
    return path

# Health check accessible at /health and /
@app.get("/health")
@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/tts")
def tts_single():
    """
    Body: { "text": "hello", "lang": "en", "slow": false, "filename": "voice.mp3" }
    Returns: audio/mpeg
    """
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    lang = data.get("lang", "en")
    slow = bool(data.get("slow", False))
    filename = data.get("filename", "speech.mp3")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    mp3_path = tts_to_cached_mp3(text, lang=lang, slow=slow)
    return send_file(mp3_path, mimetype="audio/mpeg", as_attachment=False, download_name=filename)

@app.post("/tts-batch")
def tts_batch():
    """
    Body:
    {
      "items":[
        {"scene":1, "dialogue":"What a beautiful day!"},
        {"scene":2, "dialogue":"Let's go!"}
      ],
      "lang":"en",
      "slow": false
    }
    Returns: application/zip (mp3s + manifest.json)
    """
    data = request.get_json(silent=True) or {}
    items = data.get("items") or []
    lang = data.get("lang", "en")
    slow = bool(data.get("slow", False))

    if not items:
        return jsonify({"error":"items[] is empty"}), 400

    # Build zip in-memory
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as z:
        manifest = []
        for idx, item in enumerate(items, start=1):
            dialogue = (item.get("dialogue") or "").strip()
            scene = item.get("scene", idx)
            if not dialogue:
                continue
            mp3_path = tts_to_cached_mp3(dialogue, lang=lang, slow=slow)
            mp3_name = f"scene_{scene:03d}.mp3"
            z.write(mp3_path, arcname=mp3_name)
            manifest.append({"scene": scene, "file": mp3_name, "text": dialogue})
        # Add manifest.json
        z.writestr("manifest.json", __import__("json").dumps(manifest, ensure_ascii=False, indent=2))

    buf.seek(0)
    return send_file(buf, mimetype="application/zip", as_attachment=True, download_name="tts_batch.zip")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

"""Local web UI: drop PDFs, type a text, get protected copies in ~/Downloads.

The server only listens on 127.0.0.1, so nothing is reachable from outside
your computer, and files are never sent anywhere.
"""

import threading
import webbrowser
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from watermark import watermark_pdf

HOST = "127.0.0.1"
PORT = 5173
DOWNLOADS = Path.home() / "Downloads"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200 MB per request


def unique_path(folder, stem, suffix=".pdf"):
    path = folder / f"{stem}{suffix}"
    i = 2
    while path.exists():
        path = folder / f"{stem} ({i}){suffix}"
        i += 1
    return path


@app.get("/")
def index():
    return render_template("index.html", downloads=str(DOWNLOADS))


@app.post("/protect")
def protect():
    text = request.form.get("text", "").strip()
    if not text:
        return jsonify(error="Please type a watermark text."), 400

    files = request.files.getlist("files")
    if not files:
        return jsonify(error="Please add at least one PDF."), 400

    try:
        opacity = min(max(float(request.form.get("opacity", 25)) / 100, 0.05), 1)
        font_size = min(max(int(request.form.get("font_size", 28)), 8), 120)
    except ValueError:
        return jsonify(error="Invalid settings."), 400
    color = request.form.get("color", "#808080")
    password = request.form.get("password") or None

    DOWNLOADS.mkdir(exist_ok=True)
    results = []
    for f in files:
        name = Path(f.filename or "document.pdf").name
        try:
            data = watermark_pdf(
                f.read(), text, opacity=opacity, font_size=font_size,
                color=color, password=password,
            )
            out = unique_path(DOWNLOADS, f"{Path(name).stem}_protected")
            out.write_bytes(data)
            results.append({"name": name, "ok": True, "output": out.name})
        except Exception as exc:  # report per-file errors, keep going
            results.append({"name": name, "ok": False, "error": str(exc)})

    return jsonify(results=results, folder=str(DOWNLOADS))


def main():
    url = f"http://{HOST}:{PORT}"
    print(f"Local PDF watermark running at {url}  (Ctrl+C to stop)")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    app.run(host=HOST, port=PORT, debug=False)


if __name__ == "__main__":
    main()

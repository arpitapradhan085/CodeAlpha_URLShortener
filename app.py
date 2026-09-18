"""
Simple URL Shortener
CodeAlpha Backend Development Internship - Task 1
"""

import re
import sqlite3
import string
import random
from datetime import datetime, timezone

from flask import Flask, request, jsonify, redirect, render_template, g, abort

app = Flask(__name__)

DATABASE = "shortener.db"
SHORT_CODE_LENGTH = 6
SHORT_CODE_CHARS = string.ascii_letters + string.digits

URL_REGEX = re.compile(
    r"^(https?://)"
    r"([A-Za-z0-9.-]+)"
    r"(\.[A-Za-z]{2,})"
    r"(:\d+)?"
    r"(/.*)?$"
)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        db.commit()


def is_valid_url(url: str) -> bool:
    return bool(URL_REGEX.match(url.strip()))


def generate_short_code(length: int = SHORT_CODE_LENGTH) -> str:
    db = get_db()
    while True:
        code = "".join(random.choices(SHORT_CODE_CHARS, k=length))
        existing = db.execute(
            "SELECT 1 FROM urls WHERE short_code = ?", (code,)
        ).fetchone()
        if not existing:
            return code


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json(silent=True) or request.form

    original_url = (data.get("url") or "").strip()
    custom_code = (data.get("custom_code") or "").strip()

    if not original_url:
        return jsonify({"error": "The 'url' field is required."}), 400

    if not is_valid_url(original_url):
        return jsonify({"error": "Please provide a valid http:// or https:// URL."}), 400

    db = get_db()

    if custom_code:
        if not re.match(r"^[A-Za-z0-9_-]{3,20}$", custom_code):
            return jsonify({
                "error": "custom_code must be 3-20 characters (letters, numbers, - or _)."
            }), 400
        exists = db.execute(
            "SELECT 1 FROM urls WHERE short_code = ?", (custom_code,)
        ).fetchone()
        if exists:
            return jsonify({"error": "That custom code is already taken."}), 409
        short_code = custom_code
    else:
        existing = db.execute(
            "SELECT short_code FROM urls WHERE original_url = ?", (original_url,)
        ).fetchone()
        if existing:
            short_code = existing["short_code"]
            return jsonify({
                "short_code": short_code,
                "short_url": request.host_url + short_code,
                "original_url": original_url,
                "note": "This URL was already shortened."
            }), 200
        short_code = generate_short_code()

    db.execute(
        "INSERT INTO urls (short_code, original_url, created_at) VALUES (?, ?, ?)",
        (short_code, original_url, datetime.now(timezone.utc).isoformat()),
    )
    db.commit()

    return jsonify({
        "short_code": short_code,
        "short_url": request.host_url + short_code,
        "original_url": original_url,
    }), 201


@app.route("/api/stats/<short_code>")
def stats(short_code):
    db = get_db()
    row = db.execute(
        "SELECT * FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "Short code not found."}), 404
    return jsonify({
        "short_code": row["short_code"],
        "original_url": row["original_url"],
        "created_at": row["created_at"],
        "clicks": row["clicks"],
    })


@app.route("/api/urls")
def list_urls():
    db = get_db()
    rows = db.execute("SELECT * FROM urls ORDER BY id DESC").fetchall()
    return jsonify([
        {
            "short_code": r["short_code"],
            "original_url": r["original_url"],
            "created_at": r["created_at"],
            "clicks": r["clicks"],
        }
        for r in rows
    ])


@app.route("/<short_code>")
def redirect_to_url(short_code):
    db = get_db()
    row = db.execute(
        "SELECT * FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()

    if row is None:
        abort(404)

    db.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,)
    )
    db.commit()

    return redirect(row["original_url"])


@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not found"}), 404
    return render_template("index.html", error="That short link doesn't exist."), 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)

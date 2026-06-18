from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harcamalar.db")

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS harcamalar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                baslik TEXT NOT NULL,
                tutar REAL NOT NULL,
                kategori TEXT NOT NULL,
                tarih TEXT NOT NULL
            )
        """)

@app.route("/")
def index():
    with get_db() as conn:
        harcamalar = conn.execute(
            "SELECT * FROM harcamalar ORDER BY tarih DESC"
        ).fetchall()
        toplam = conn.execute(
            "SELECT COALESCE(SUM(tutar), 0) FROM harcamalar"
        ).fetchone()[0]
    return render_template("index.html", harcamalar=harcamalar, toplam=toplam)

@app.route("/ekle", methods=["POST"])
def ekle():
    baslik = request.form["baslik"]
    tutar = request.form["tutar"]
    kategori = request.form["kategori"]
    tarih = request.form["tarih"] or datetime.today().strftime("%Y-%m-%d")
    with get_db() as conn:
        conn.execute(
            "INSERT INTO harcamalar (baslik, tutar, kategori, tarih) VALUES (?, ?, ?, ?)",
            (baslik, float(tutar), kategori, tarih)
        )
    return redirect(url_for("index"))

@app.route("/sil/<int:id>")
def sil(id):
    with get_db() as conn:
        conn.execute("DELETE FROM harcamalar WHERE id = ?", (id,))
    return redirect(url_for("index"))



init_db()
if __name__ == "__main__":
    app.run(debug=True)

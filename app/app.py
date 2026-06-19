import os
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"), cursor_factory=RealDictCursor)
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS peliculas (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            anio INTEGER NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "version": "1.0"}), 200

@app.route('/peliculas', methods=['GET'])
def get_peliculas():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM peliculas ORDER BY id")
    peliculas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(list(peliculas)), 200

@app.route('/peliculas/<int:id>', methods=['GET'])
def get_pelicula(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM peliculas WHERE id = %s", (id,))
    pelicula = cur.fetchone()
    cur.close()
    conn.close()
    if pelicula is None:
        return jsonify({"error": "Pelicula no encontrada"}), 404
    return jsonify(dict(pelicula)), 200

@app.route('/peliculas', methods=['POST'])
def create_pelicula():
    data =
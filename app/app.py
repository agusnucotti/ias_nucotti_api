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
    return jsonify({"status": "ok"}), 200

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
    data = request.get_json()
    if not data or 'titulo' not in data or 'anio' not in data:
        return jsonify({"error": "titulo y anio son requeridos"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO peliculas (titulo, anio) VALUES (%s, %s) RETURNING *",
        (data['titulo'], data['anio'])
    )
    nueva = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(nueva)), 201

@app.route('/peliculas/<int:id>', methods=['DELETE'])
def delete_pelicula(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM peliculas WHERE id = %s RETURNING *", (id,))
    eliminada = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if eliminada is None:
        return jsonify({"error": "Pelicula no encontrada"}), 404
    return jsonify({"mensaje": "Pelicula eliminada"}), 200

if __name__ == '__main__':
    init_db()
    debug = os.environ.get('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=5000, debug=debug)  # nosec B104

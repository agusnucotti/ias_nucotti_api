import os
from flask import Flask, jsonify

app = Flask(_name_)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/peliculas', methods=['GET'])
def get_peliculas():
    peliculas = [
        {"id": 1, "titulo": "Inception", "año": 2010},
        {"id": 2, "titulo": "Interstellar", "año": 2014}
    ]
    return jsonify(peliculas), 200

@app.route('/peliculas/<int:id>', methods=['GET'])
def get_pelicula(id):
    return jsonify({"id": id, "titulo": "Inception", "año": 2010}), 200

if _name_ == '_main_':
    debug = os.environ.get('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=5000, debug=debug)
    
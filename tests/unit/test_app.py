import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.app import app

def test_health():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200

def test_get_peliculas():
    client = app.test_client()
    response = client.get('/peliculas')
    assert response.status_code == 200

def test_get_pelicula_por_id():
    client = app.test_client()
    response = client.get('/peliculas/1')
    assert response.status_code == 200
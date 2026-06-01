import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(_file_), '..', '..'))

from app.app import app

def test_health_retorna_json():
    client = app.test_client()
    response = client.get('/health')
    data = response.get_json()
    assert data['status'] == 'ok'

def test_peliculas_retorna_lista():
    client = app.test_client()
    response = client.get('/peliculas')
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
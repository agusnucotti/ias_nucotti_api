import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(_file_), '..', '..'))

from app.app import app

def test_health_disponible():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200

def test_ruta_inexistente_retorna_404():
    client = app.test_client()
    response = client.get('/ruta-que-no-existe')
    assert response.status_code == 404
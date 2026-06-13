import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

with patch('psycopg2.connect') as mock_connect:
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    mock_cursor.fetchone.return_value = None
    from app.app import app

def test_health_no_expone_info_sensible():
    client = app.test_client()
    response = client.get('/health')
    data = response.get_json()
    assert 'password' not in str(data)
    assert 'secret' not in str(data)

def test_endpoint_invalido_retorna_404():
    client = app.test_client()
    response = client.get('/ruta-invalida')
    assert response.status_code == 404

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from unittest.mock import patch, MagicMock
from app.app import app

def test_health_retorna_json():
    client = app.test_client()
    response = client.get('/health')
    data = response.get_json()
    assert data['status'] == 'ok'

def test_peliculas_retorna_lista():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"id": 1, "titulo": "Test", "anio": 2020}]

    with patch('app.app.get_db', return_value=mock_conn):
        client = app.test_client()
        response = client.get('/peliculas')
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0
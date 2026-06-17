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

def test_health_retorna_json():
    client = app.test_client()
    response = client.get('/health')
    data = response.get_json()
    assert data['status'] == 'ok'

def test_peliculas_retorna_lista():
    with patch('app.app.get_db') as mock_get_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        client = app.test_client()
        response = client.get('/peliculas')
        data = response.get_json()
        assert isinstance(data, list)

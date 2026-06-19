import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from unittest.mock import patch, MagicMock
from app.app import app

def test_health():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200

def test_get_peliculas():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    with patch('app.app.get_db', return_value=mock_conn):
        client = app.test_client()
        response = client.get('/peliculas')
        assert response.status_code == 200

def test_get_pelicula_por_id():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {"id": 1, "titulo": "Test", "anio": 2020}

    with patch('app.app.get_db', return_value=mock_conn):
        client = app.test_client()
        response = client.get('/peliculas/1')
        assert response.status_code == 200
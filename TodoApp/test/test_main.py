from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app)

def test_healthz():
    response = client.get('/healthz')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Ok'}
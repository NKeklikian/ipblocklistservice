import pytest
import time
from app import app as my_app
from app.home.ip_blocklist_service import IpBlocklistService
import redis
from app.home.config import REDIS_HOST, REDIS_PORT
from app.home.constants import BLOCKLIST_NAME

@pytest.fixture
def app():
    my_app.config.update({"TESTING": True})
    yield my_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


redis_test_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def test_safe_ip(client):
    response = client.get("/api/ips/0.0.0.0")
    assert response.data == b'{"is_in_blocklist":false}\n'
    assert response.status_code == 200


def test_blocklisted_ip(client):
    service = IpBlocklistService
    redis_test_instance.sadd(BLOCKLIST_NAME, '103.251.167.20')
    response = client.get("/api/ips/103.251.167.20")
    assert response.data == b'{"is_in_blocklist":true}\n'
    assert response.status_code == 200


def test_invalid_ip(client):
    response = client.get("/api/ips/my_sample")
    assert response.data == b'{"message":"Invalid IP","trace":null}\n'
    assert response.status_code == 422


def test_empty_ip(client):
    response = client.get("/api/ips/")
    assert response.status_code == 404


def test_wrong_method(client):
    response = client.post("/api/ips/0.0.0.0")
    assert response.status_code == 405

# Tests: request OK, request false, parametro vacio, parametro roto (ip mal formateada)
# , hacer post/put/etc
# mockear la api de git y hacer que rompe
# testear errores en las funciones internas
# ponerle puerto 000 a flask para que rompa
# armar un endpoint para on demand testear las funciones internas

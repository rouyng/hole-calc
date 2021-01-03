from config import TestConfig
from main import app as hc_app
import pytest

"""
Tests for the flask app

These tests are integration tests of the user-accessible functionality exposed by the flask app
"""


@pytest.fixture
def flask_app():
    app = hc_app
    app.config.from_object(TestConfig)
    yield app


@pytest.fixture
def client(flask_app):
    return flask_app.test_client()


def test_heartbeat(flask_app, client):
    """test whether the flask app starts successfully and the heartbeat route works"""
    response = client.get('/heartbeat')
    assert response.status_code == 200
    assert response.data == b'OK'


def test_index(flask_app, client):
    response = client.get('/')
    assert response.status_code == 200


def test_about(flask_app, client):
    response = client.get('/about/')
    assert response.status_code == 200


def test_guide(flask_app, client):
    response = client.get('/guide/')
    assert response.status_code == 200


def test_three_pin_calculation_in(flask_app, client):
    post_data = {"pin1": "1",
                 "pin1_class": "XX",
                 "pin1_sign": "+",
                 "pin2": "2",
                 "pin2_class": "XX",
                 "pin2_sign": "+",
                 "pin3": "3",
                 "pin3_class": "XX",
                 "pin3_sign": "+",
                 "units": "in",
                 "precision": "0.001"}
    response = client.post('/', data=post_data)
    assert b"6.000" in response.data


def test_pin_size_calculation_in(flask_app, client):
    post_data = {"pin_dia": "1",
                 "pin_class": "ZZ",
                 "pin_sign": "-",
                 "units": "in"}
    response = client.post('/pinsize', data=post_data)
    assert b"0.999760" in response.data
    assert b"1.000000" in response.data


def test_pin_size_calculation_mm(flask_app, client):
    post_data = {"pin_dia": "65",
                 "pin_class": "ZZ",
                 "pin_sign": "-",
                 "units": "mm"}
    response = client.post('/pinsize', data=post_data)
    assert b"64.9900" in response.data
    assert b"65.0000" in response.data


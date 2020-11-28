from config import TestConfig
from app import app as hc_app
import pytest

"""
Tests for the flask app

These tests are functional tests of the user-accessible functionality exposed by the flask app
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
    assert b'A bore measurement calculator for machinists' in response.data


def test_calculation(flask_app, client):
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
    response = client.post(data=post_data)
    assert b"6.000" in response.data

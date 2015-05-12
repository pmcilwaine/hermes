# /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytest
import logging
from mock import patch, MagicMock
from hermes_cms.app import create_app


def app():
    """

    :return: flask.Flask
    """
    return create_app().test_client()


@pytest.fixture
def blueprint_config():
    instance = MagicMock(name='Registry')
    instance.get.return_value = {
        'blueprint': [
            {
                'name': 'hermes_cms.views.main',
                'from': 'route'
            }
        ]
    }

    return instance


@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_health(config, db_connect_mock, blueprint_config, caplog):

    caplog.setLevel(logging.DEBUG)
    config.return_value = blueprint_config
    db_connect_mock.return_value = None

    expected = json.dumps({'status': 'ok'})
    response = app().get('/health')

    assert response.data == expected
    assert response.status_code == 200


@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_get_login(config, db_connect_mock, blueprint_config, caplog):

    caplog.setLevel(logging.DEBUG)
    config.return_value = blueprint_config
    db_connect_mock.return_value = None

    response = app().get('/login')
    assert response.status_code == 200


@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
@patch('hermes_cms.views.main.Auth')
def test_post_login_invalid(auth, config, db_connect_mock, blueprint_config, caplog):

    caplog.setLevel(logging.DEBUG)
    config.return_value = blueprint_config
    db_connect_mock.return_value = None

    auth.get_by_login.return_value = False

    response = app().post('/login', data={
        'email': 'bad@example.org',
        'password': 'password'
    })

    assert response.status_code == 400


@patch('hermes_cms.app.Registry')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.views.main.Auth')
def test_post_login_valid(auth, db_connect_mock, config, blueprint_config, caplog):

    caplog.setLevel(logging.DEBUG)
    config.return_value = blueprint_config
    db_connect_mock.return_value = None

    auth.get_by_login.return_value = True

    response = app().post('/login', data={
        'email': 'bad@example.org',
        'password': 'password'
    })

    assert response.status_code == 302


@patch('hermes_cms.views.main.Auth')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_logout_ok(config, db_connect_mock, auth_mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    auth_mock.delete_session.return_value = True

    response = app().get('/logout')
    assert response.status_code == 302


@patch('hermes_cms.views.main.Auth')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_logout_fail(config, db_connect_mock, auth_mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    auth_mock.delete_session.return_value = False

    response = app().get('/logout')
    assert response.status_code == 400

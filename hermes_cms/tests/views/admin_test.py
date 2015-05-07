# /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from mock import patch, MagicMock
from hermes_cms.app import create_app


def app():
    """

    :return: flask.Flask
    """
    return create_app().test_client()


@pytest.fixture
def blueprint_config():
    instance = MagicMock(name='Config')
    instance.get.return_value = [{
        'name': 'hermes_cms.views.admin',
        'from': 'route'
    }]

    return instance

@patch('hermes_cms.core.auth.session')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_index(config, db_connect_mock, session_mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    session_mock.get.return_value = True

    response = app().get('/admin/')
    assert response.status_code == 200
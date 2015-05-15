# /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import json
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
                'name': 'hermes_cms.views.admin',
                'from': 'route'
            }
        ]
    }

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


@patch('hermes_cms.views.admin.User')
@patch('hermes_cms.views.admin.UserValidation')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_user_save(config, db_connect_mock, validation_mock, user_mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    validation_mock.validate.return_value = True
    user_mock.save.return_value = MagicMock(
        uid='some-uid',
        email='test@example.org',
        first_name='',
        last_name=''
    )

    expected = {
        'uid': 'some-uid',
        'email': 'test@example.org',
        'first_name': '',
        'last_name': ''
    }

    response = app().post('/admin/user', data=json.dumps({
        'email': 'test@example.org',
        'password': 'password'
    }), content_type='application/json')

    assert json.loads(response.data) == expected
    assert response.status_code == 200


@patch('hermes_cms.views.admin.UserValidation')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_user_save_invalid_form(config, db_connect_mock, validation_mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    validation = validation_mock.return_value

    validation.validate.return_value = False
    validation.errors.return_value = {
        'email': 'Email is required',
        'password': 'Password is required'
    }

    expected = {
        'fields': {
            'email': 'Email is required',
            'password': 'Password is required'
        }
    }

    response = app().post('/admin/user', data=json.dumps({
        'email': '',
        'password': '',
        'first_name': '',
        'last_name': ''
    }), content_type='application/json')

    assert json.loads(response.data) == expected
    assert response.status_code == 400


@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_user_save_invalid_request(config, db_connect_mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None

    expected = {
        'title': 'Invalid Request',
        'message': 'Invalid request was made'
    }

    response = app().post('/admin/user', data=None)
    assert json.loads(response.data) == expected
    assert response.status_code == 400


@patch('hermes_cms.views.admin.User')
@patch('hermes_cms.views.admin.UserValidation')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_user_update(config, db_connect_mock, validation_mock, user_mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    validation_mock.validate.return_value = True

    user_mock.save.return_value = MagicMock(
        uid='abcdef',
        email='test@example.org',
        first_name='Test',
        last_name='User'
    )

    response = app().put('/admin/user/abcdef', data=json.dumps({
        'email': 'test@example.org',
        'password': '',
        'first_name': 'Test',
        'last_name': 'User'
    }), content_type='application/json')

    expected = {
        'uid': 'abcdef',
        'email': 'test@example.org',
        'first_name': 'Test',
        'last_name': 'User'
    }

    assert json.loads(response.data) == expected
    assert response.status_code == 200


@patch('hermes_cms.views.admin.User')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_user_get_list(config, db_connect_mock, user_mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    user_mock.selectBy.return_value = [
        MagicMock(email='test@example.org', first_name='Test', last_name='User', uid='some-id')
    ]

    expected = {
        'users': [
            {
                'uid': 'some-id',
                'email': 'test@example.org',
                'first_name': 'Test',
                'last_name': 'User'
            }
        ]
    }

    response = app().get('/admin/user')
    assert json.loads(response.data) == expected
    assert response.status_code == 200


@pytest.fixture
def documents():
    d1 = MagicMock(gid=1, url='/', type='Page', uuid='some-id', path='1/',
                   published=True, archived=False, menutitle='Homepage', show_in_menu=True)
    d1.name = 'Homepage'

    d2 = MagicMock(gid=2, url='/second-page', type='Page', uuid='some-id', path='2/',
                   published=True, archived=False, menutitle='Second Page', show_in_menu=True)
    d2.name = 'Second Page'

    return [d1, d2]


@patch('hermes_cms.views.admin.Document')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_document_list_first_page_no_children(config, db_connect_mock, document_mock, documents, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None

    document_mock.selectBy.return_value = documents

    expected = {
        'documents': [
            {
                'gid': 1,
                'name': 'Homepage',
                'url': '/',
                'type': 'Page'
            },
            {
                'gid': 2,
                'name': 'Second Page',
                'url': '/second-page',
                'type': 'Page'
            }
        ],
        'meta': {
            'offset': 0,
            'limit': 100
        }
    }

    response = app().get('/admin/document')
    assert response.status_code == 200
    assert json.loads(response.data) == expected

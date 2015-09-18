# /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import json
from mock import patch, MagicMock
from utils import mocks
mocks.mock_modules()
from hermes_cms.core.auth import Auth
from hermes_cms.app import create_app


def app():
    """

    :return: flask.Flask
    """
    return create_app().test_client()


@pytest.fixture
def admin_rules_config():
    instance = MagicMock(name='Registry')
    instance.get.return_value = {
        'rules': [
            {
                "name": "job",
                "url": "/job",
                "module_name": "hermes_cms.controller.admin.job",
                "class_name": "Job",
                "methods": ["GET"]
            },
            {
                "name": "user",
                "module_name": "hermes_cms.controller.admin.user",
                "class_name": "User",
                "urls": [
                    {
                        "url": "/user",
                        "methods": ["GET", "POST"]
                    },
                    {
                        "url": "/user/<int:user_id>",
                        "methods": ["GET", "PUT", "DELETE"]
                    }
                ]
            },
            {
                "name": "document",
                "module_name": "hermes_cms.controller.admin.document",
                "class_name": "Document",
                "urls": [
                    {
                        "url": "/document",
                        "methods": ["GET", "POST"]
                    },
                    {
                        "url": "/document/<document_id>",
                        "methods": ["GET", "PUT", "DELETE"]
                    }
                ]
            }
        ]
    }

    return instance


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


@patch.object(Auth, 'has_permission')
@patch('hermes_cms.views.admin.Registry')
@patch('hermes_cms.core.auth.session')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_index(config, db_connect_mock, session_mock, registry_mock, permission_mock, blueprint_config,
               admin_rules_config):
    config.return_value = blueprint_config
    registry_mock.return_value = admin_rules_config
    db_connect_mock.return_value = None
    session_mock.get.return_value = True
    permission_mock.return_value = True

    response = app().get('/admin/')
    assert response.status_code == 200


@patch('hermes_cms.views.admin.Registry')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.user.UserDB')
@patch('hermes_cms.controller.admin.user.UserValidation')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_user_save(config, db_connect_mock, validation_mock, user_mock, permission_mock, _mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    validation_mock.validate.return_value = True
    permission_mock.return_value = True

    user_mock.save.return_value = MagicMock(
        id=1,
        email='test@example.org',
        first_name='',
        last_name=''
    )

    expected = {
        'id': 1,
        'email': 'test@example.org',
        'first_name': '',
        'last_name': '',
        'notify_msg': {
            'title': 'Added User',
            'type': 'success',
            'message': 'User test@example.org has been added'
        }
    }

    response = app().post('/admin/user', data=json.dumps({
        'email': 'test@example.org',
        'password': 'password'
    }), content_type='application/json')

    assert json.loads(response.data) == expected
    assert response.status_code == 200


@patch('hermes_cms.views.admin.Registry')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.user.UserValidation')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_user_save_invalid_form(config, db_connect_mock, validation_mock, permission_mock, _mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    validation = validation_mock.return_value
    permission_mock.return_value = True

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


@patch('hermes_cms.views.admin.Registry')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_user_save_invalid_request(config, db_connect_mock, permission_mock, _mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    permission_mock.return_value = True

    expected = {
        'title': 'Invalid Request',
        'message': 'Invalid request was made'
    }

    response = app().post('/admin/user', data=None)
    print response
    assert json.loads(response.data) == expected
    assert response.status_code == 400


@patch('hermes_cms.views.admin.Registry')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.user.UserDB')
@patch('hermes_cms.controller.admin.user.UserValidation')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_user_update(config, db_connect_mock, validation_mock, user_mock, permission_mock, _mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    validation_mock.validate.return_value = True
    permission_mock.return_value = True

    user_mock.save.return_value = MagicMock(
        id=2,
        email='test@example.org',
        first_name='Test',
        last_name='User'
    )

    response = app().put('/admin/user/2', data=json.dumps({
        'email': 'test@example.org',
        'password': '',
        'first_name': 'Test',
        'last_name': 'User'
    }), content_type='application/json')

    expected = {
        'id': 2,
        'email': 'test@example.org',
        'first_name': 'Test',
        'last_name': 'User',
        'notify_msg': {
            'title': 'Modified User',
            'type': 'success',
            'message': 'User test@example.org has been modified'
        }
    }

    assert json.loads(response.data) == expected
    assert response.status_code == 200


@patch('hermes_cms.core.auth.session')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.views.admin.Registry')
@patch('hermes_cms.controller.admin.user.UserDB')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_user_get_list(config, db_connect_mock, user_mock, _mock, permission_mock, session_mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    user_mock.selectBy.return_value = [
        MagicMock(email='test@example.org', first_name='Test', last_name='User', id=3)
    ]
    permission_mock.return_value = True

    expected = {
        'users': [
            {
                'id': 3,
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
    d1 = MagicMock(id=1, url='/', type='Page', uuid='some-id', path='1/',
                   published=True, archived=False, menutitle='Homepage', show_in_menu=True)
    d1.name = 'Homepage'

    d2 = MagicMock(id=2, url='/second-page', type='Page', uuid='some-id-2', path='2/',
                   published=True, archived=False, menutitle='Second Page', show_in_menu=True)
    d2.name = 'Second Page'

    return [d1, d2]


@patch('hermes_cms.views.admin.Registry')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.document.DocumentDB')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_document_list_first_page_no_children(config, db_connect_mock, document_mock, permission_mock, _mock,
                                              documents, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    permission_mock.return_value = True

    document_mock.query.return_value = documents

    expected = {
        'documents': [
            {
                'id': 1,
                'uuid': 'some-id',
                'name': 'Homepage',
                'url': '/',
                'type': 'Page',
                'path': '1/',
                'published': True
            },
            {
                'id': 2,
                'uuid': 'some-id-2',
                'name': 'Second Page',
                'url': '/second-page',
                'type': 'Page',
                'path': '2/',
                'published': True
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


@patch('hermes_cms.views.admin.Registry')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.document.DocumentValidation')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_document_validate_fail(config, db_connect_mock, validation_mock, permission_mock, _mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    validation_instance = validation_mock.return_value
    permission_mock.return_value = True

    validation_instance.validate.return_value = False
    validation_instance.errors.return_value = {
        'document': {
            'name': 'Must enter name',
            'url': 'Must enter a URL',
            'type': 'Must select a type'
        }
    }

    response = app().post('/admin/document?validate=true', data=json.dumps({}))
    expected = {
        'fields': {
            'document': {
                'name': 'Must enter name',
                'url': 'Must enter a URL',
                'type': 'Must select a type'
            }
        }
    }

    print response
    assert json.loads(response.data) == expected
    assert response.status_code == 400


@patch('hermes_cms.views.admin.Registry')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.document.DocumentValidation')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_document_validate_success(config, db_connect_mock, validation_mock, permission_mock, _mock, blueprint_config):
    config.return_value = blueprint_config
    db_connect_mock.return_value = None
    validation_mock.validate.return_value = True
    permission_mock.return_value = True

    response = app().post('/admin/document?validate=true', data=json.dumps({
        'document': {
            'name': 'First Document',
            'url': '/first-document',
            'type': 'Page',
            'parent': None
        }
    }), content_type='application/json')

    expected = {
        'document': {
            'name': 'First Document',
            'url': '/first-document',
            'type': 'Page',
            'parent': None
        }
    }

    assert json.loads(response.data) == expected
    assert response.status_code == 200

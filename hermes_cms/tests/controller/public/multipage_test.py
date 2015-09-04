# /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from mock import patch, MagicMock, mock_open
from hermes_cms.app import create_app


def app():
    """

    :return: flask.Flask
    """
    return create_app().test_client()


@pytest.fixture
def config():
    instance = MagicMock(name='Registry')
    instance.get.return_value = {
        'blueprint': [
            {
                "name": "hermes_cms.views.main",
                "from": "route"
            }
        ]
    }
    return instance


@patch('hermes_cms.core.route.Document')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_redirect_multipage(registry_mock, db_connect_mock, document_mock, config):
    registry_mock.return_value = config
    db_connect_mock.return_value = None

    document_mock.get_document.return_value = {
        'document': {
            'uuid': 'multipage',
            'url': 'multipage'
        }
    }
    document_mock.select.return_value.getOne.return_value = MagicMock(
        uuid='multipage',
        type='MultiPage'
    )

    response = app().get('/multipage')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/multipage/'


@patch('hermes_cms.controller.public.multipage.mimetypes')
@patch('hermes_cms.controller.public.multipage.os')
@patch('hermes_cms.core.route.Document')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
@patch('hermes_cms.controller.public.multipage.Registry')
def test_no_redirect_for_child_item(multipage_config, registry_mock, db_connect_mock, document_mock, os_mock,
                                    mimetypes_mock, config):
    registry_mock.return_value = config
    db_connect_mock.return_value = None

    os_mock.path.abspath.return_value = 'test-doc.html'
    os_mock.path.return_value.exists.return_value = True
    mimetypes_mock.guess_type.return_value = ('text/html', None)

    # multipage_config

    document_mock.get_document.return_value = {
        'document': {
            'uuid': 'multipage',
            'url': 'multipage'
        }
    }
    document_mock.select.return_value.getOne.return_value = MagicMock(
        uuid='multipage',
        type='MultiPage'
    )

    m = mock_open(read_data='Contents')
    with patch('__builtin__.open', m, create=True):

        response = app().get('/multipage/test-doc.html')
        assert response.data == 'Contents'
        assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
        assert response.status_code == 200

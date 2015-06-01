# /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
from mock import patch
from hermes_cms.controller import Page


@pytest.fixture(autouse=True)
def config_fixture():
    return {
        'template_modules': [
            'data'
        ],
        'templates': {
            'test': 'test.html'
        }
    }


@pytest.fixture(autouse=True)
def document_fixture():
    return {
        'document': {
            'url': 'the-new-page',
            'name': 'The New Page',
            'menutitle': 'New Page'
        },
        'page': {
            'content': 'Some content to be displayed',
            'template': 'test'
        }
    }


@patch('hermes_cms.controller.page.navigation')
@patch('hermes_cms.controller.page.resource_filename')
def test_get_page(resource_mock, navigation_mock, document_fixture, config_fixture):
    resource_mock.return_value = os.path.join(os.path.dirname(__file__), 'data')
    navigation_mock.return_value = []

    page = Page(document_fixture, config_fixture)
    response = page.get()

    expected = """
<h1>New Page</h1>
<p>Test Page</p>
<p>Some content to be displayed</p>
    """

    assert response.status_code == 200
    assert response.content_type == 'text/html'
    assert response.data == expected.strip()

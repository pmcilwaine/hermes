# /usr/bin/env python
# -*- coding: utf-8 -*-

from mock import patch
from hermes_cms.core.route import route


@patch('hermes_cms.helpers.page.Document')
@patch('hermes_cms.core.route.Document')
def test_no_page_found(document_mock, nav_mock):
    document_mock.select.return_value.getOne.return_value = None

    response = route('abc-def')
    assert response.status_code == 404


@patch('hermes_cms.core.route.Document')
def test_no_homepage_found(document_mock):
    document_mock.select.return_value.getOne.return_value = None
    response = route('index')

    assert response.status_code == 302
    assert response.headers['Location'] == '/login'

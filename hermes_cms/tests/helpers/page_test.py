# /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from mock import MagicMock, patch
from hermes_cms.helpers.page import navigation


def create_document_mock(**kwargs):
    parent = kwargs.pop('parent', None)
    mock = MagicMock(**kwargs)
    mock.parent = parent
    return mock


@pytest.fixture
def single_level_nav():
    results = [create_document_mock(
        gid=1,
        url='/',
        path='1/',
        parent=None,
        published=True,
        menutitle='Homepage'
    ), create_document_mock(
        gid=2,
        url='/first-page',
        path='2/',
        parent=None,
        published=True,
        menutitle='First Page'
    ), create_document_mock(
        gid=3,
        url='/second-page',
        path='3/',
        parent=None,
        published=True,
        menutitle='Second Page'
    )]

    return results


@pytest.fixture
def two_level_nav():
    results = [create_document_mock(
        gid=1,
        url='/',
        path='1/',
        parent=None,
        published=True,
        menutitle='Homepage'
    ), create_document_mock(
        gid=2,
        url='/first-page',
        path='2/',
        parent=None,
        published=True,
        menutitle='First Page'
    ), create_document_mock(
        gid=3,
        url='/second-page',
        path='3/',
        parent=None,
        published=True,
        menutitle='Second Page'
    ), create_document_mock(
        gid=4,
        url='/second-page/first-node',
        path='3/4/',
        parent=3,
        published=True,
        menutitle='First Node'
    ), create_document_mock(
        gid=5,
        url='/second-page/second-node',
        path='3/5/',
        parent=3,
        published=True,
        menutitle='Second Node'
    )]

    return results


@patch('hermes_cms.helpers.page.Document')
def test_single_level_navigation(document_mock, single_level_nav):
    document_mock.select.return_value.filter.return_value = single_level_nav

    expected = [
        {
            'url': '/',
            'menutitle': 'Homepage',
            'current': True,
            'children': []
        },
        {
            'url': '/first-page',
            'menutitle': 'First Page',
            'current': False,
            'children': []
        },
        {
            'url': '/second-page',
            'menutitle': 'Second Page',
            'current': False,
            'children': []
        }
    ]

    assert navigation({'document': {'path': '1/'}}) == expected


@patch('hermes_cms.helpers.page.Document')
def test_second_level_navigation(document_mock, two_level_nav):
    document_mock.select.return_value.filter.return_value = two_level_nav

    expected = [
        {
            'url': '/',
            'menutitle': 'Homepage',
            'current': False,
            'children': []
        },
        {
            'url': '/first-page',
            'menutitle': 'First Page',
            'current': False,
            'children': []
        },
        {
            'url': '/second-page',
            'menutitle': 'Second Page',
            'current': True,
            'children': [
                {
                    'url': '/second-page/first-node',
                    'menutitle': 'First Node',
                    'current': True,
                    'children': []
                },
                {
                    'url': '/second-page/second-node',
                    'menutitle': 'Second Node',
                    'current': False,
                    'children': []
                }
            ]
        }
    ]

    assert navigation({'document': {'path': '3/4/'}}) == expected

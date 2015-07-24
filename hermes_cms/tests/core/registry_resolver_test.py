# /usr/bin/env python
# -*- coding: utf-8 -*-
from hermes_cms.core.registry_resolver import RegistryResolver
from mock import patch


@patch('hermes_cms.core.registry_resolver.Registry')
def test_single_string(registry_mock):
    registry_mock.return_value.get.return_value = {
        'single': 'testing'
    }
    resolver = RegistryResolver()
    assert 'testing' == resolver.resolver('config:///test.single')


@patch('hermes_cms.core.registry_resolver.Registry')
def test_multiple_string(registry_mock):
    registry_mock.return_value.get.return_value = {
        'multiple': {
            'outer': {
                'content': 'Hello World'
            }
        }
    }
    resolver = RegistryResolver()
    assert 'Hello World' == resolver.resolver('config:///test.multiple.outer.content')


@patch('hermes_cms.core.registry_resolver.Registry')
def test_no_resolve(registry_mock):
    resolver = RegistryResolver()
    assert 'Hello World' == resolver.resolver('Hello World')

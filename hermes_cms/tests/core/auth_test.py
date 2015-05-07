# /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from hermes_cms.core.auth import Auth


@pytest.fixture
def user_mock():
    return {'permissions': ['add', 'modify', 'delete']}


def test_has_single_permission(user_mock):
    assert Auth.has_permission(user_mock, 'add') is True


def test_has_multiple_permissions(user_mock):
    assert Auth.has_permission(user_mock, ['add', 'modify', 'delete']) is True


def test_has_multiple_permissions_subset(user_mock):
    assert Auth.has_permission(user_mock, ['add', 'modify']) is True


def test_missing_permission(user_mock):
    assert Auth.has_permission(user_mock, ['restore']) is False


def test_missing_single_permission_from_set(user_mock):
    assert Auth.has_permission(user_mock, ['add', 'modify', 'delete', 'restore']) is False

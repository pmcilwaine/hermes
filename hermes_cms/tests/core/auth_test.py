# /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from mock import patch
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


@patch('hermes_cms.core.auth.session')
def test_delete_session(session_mock):
    session_mock.__contains__.return_value = True
    assert Auth.delete_session() is True
    session_mock.pop.assert_called_with('auth_user')

@patch('hermes_cms.core.auth.session')
def test_delete_session_no_session(session_mock):
    session_mock.__contains__.return_value = False
    assert Auth.delete_session() is False

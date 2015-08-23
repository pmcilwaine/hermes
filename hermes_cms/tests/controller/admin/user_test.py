# /usr/bin/env python
# -*- coding: utf-8 -*-
from hermes_cms.core.auth import Auth
from mock import patch, call, MagicMock
from hermes_cms.controller.admin.user import User


@patch('hermes_cms.core.auth.session')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.user.UserDB')
def test_delete_invalid_user_id_404(user_db, permission_mock, session_mock):
    user_db.selectBy.return_value.getOne.return_value = None
    permission_mock.return_value = True

    user = User()
    response = user.delete(user_id=1)
    assert response.status_code == 404


@patch('hermes_cms.core.auth.session')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.user.UserDB')
def test_delete_valid_user(user_db, permission_mock, session_mock):
    user = MagicMock()
    user.set = MagicMock()

    user_db.selectBy.return_value.getOne.return_value = user
    permission_mock.return_value = True

    user_ctrl = User()
    response = user_ctrl.delete(user_id=1)

    assert response.status_code == 200
    assert user.set.call_args_list == [call(archived=True)]

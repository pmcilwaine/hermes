# /usr/bin/env python
# -*- coding: utf-8 -*-
from hermes_cms.core.auth import Auth
from mock import patch, call, MagicMock
from hermes_cms.db.document import DocumentNotFound
from hermes_cms.controller.admin.restore_document import RestoreDocument


@patch('hermes_cms.core.auth.session')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.restore_document.DocumentDB')
def test_delete_invalid_document_id_404(document_db, permission_mock, session_mock):
    document_db.restore_document.side_effect = DocumentNotFound()
    permission_mock.return_value = True

    document = RestoreDocument()
    response = document.put(document_id=1)
    assert response.status_code == 404


@patch('hermes_cms.core.auth.session')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.restore_document.DocumentDB')
def test_delete_document_id(document_db, permission_mock, session_mock):
    permission_mock.return_value = True

    document = RestoreDocument()
    response = document.put(document_id=1)
    assert response.status_code == 200


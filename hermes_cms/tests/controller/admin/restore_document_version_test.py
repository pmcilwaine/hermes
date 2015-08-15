# /usr/bin/env python
# -*- coding: utf-8 -*-
from hermes_cms.core.auth import Auth
from mock import patch, call, MagicMock
from hermes_cms.controller.admin.restore_document_version import RestoreDocumentVersion


@patch('hermes_cms.core.auth.session')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.restore_document_version.DocumentDB')
def test_restore_invalid_document_404(document_db, permission_mock, session_mock):
    document_db.selectBy.return_value.getOne.return_value = None
    permission_mock.return_value = True

    document = RestoreDocumentVersion()
    response = document.put(document_id='some-uuid')
    assert response.status_code == 404


@patch('hermes_cms.controller.admin.restore_document_version.Registry')
@patch('hermes_cms.core.auth.session')
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.controller.admin.restore_document_version.session')
@patch('hermes_cms.controller.admin.restore_document_version.DocumentDB')
def test_restore_valid_doc_version(document_db, session_document_mock, permission_mock, session_mock, registry_mock):
    document_db.selectBy.return_value.getOne.return_value = MagicMock(**{
        'uuid': 'some-uuid',
        'id': 1
    })
    session_document_mock.__getitem__.return_value.get.return_value = 1
    permission_mock.return_value = True
    document_db.get_document.return_value = {'document': {'type': None}}
    registry_mock.return_value.get.return_value.get.return_value.get.return_value = {}

    document = RestoreDocumentVersion()
    response = document.put(document_id='some-uuid')
    assert response.status_code == 200

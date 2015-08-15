# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask.views import MethodView
from flask import Response, session
from hermes_cms.helpers import common
from sqlobject.sqlbuilder import DESC
from hermes_cms.core.registry import Registry
from hermes_cms.db import Document as DocumentDB
from hermes_cms.core.auth import requires_permission


class RestoreDocumentVersion(MethodView):

    @requires_permission('restore_version_document')
    def get(self, document_id=None):
        documents = []
        for document in DocumentDB.query_as_dict(DocumentDB.all(), orderBy=DESC(DocumentDB.q.created),
                                                 where=(DocumentDB.q.id == document_id)):
            document['created'] = str(document['created'])
            documents.append(document)

        if not documents:
            return Response(status=404)

        return Response(response=json.dumps({'documents': documents}),
                        content_type='application/json', status=200)

    @requires_permission('restore_version_document')
    def put(self, document_id=None):
        document = DocumentDB.selectBy(uuid=document_id).getOne(None)
        if not document:
            return Response(status=404)

        document_data = DocumentDB.get_document(document)
        document_data['id'] = document.id

        document_data['document']['user_id'] = session['auth_user'].get('id', -1)
        document = DocumentDB.save(document_data)

        document_type = document_data['document']['type']
        helper_class = Registry().get('document').get(document_type, {}).get('admin_helper', {})
        if helper_class:
            common.load_class(
                helper_class.get('document_module'),
                helper_class.get('document_class'),
                document
            ).do_work()

        return Response(response=json.dumps(document_data), status=200)

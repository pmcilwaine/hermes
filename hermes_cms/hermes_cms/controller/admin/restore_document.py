# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask.views import MethodView
from flask import Response, request
from sqlobject.sqlbuilder import DESC
from hermes_cms.core.auth import requires_permission
from hermes_cms.db import Document as DocumentDB, DocumentNotFound


class RestoreDocument(MethodView):

    # pylint: disable=no-self-use
    @requires_permission('restore_deleted_document')
    def get(self):
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))

        documents = []
        for document in DocumentDB.query(DocumentDB.all(), where=DocumentDB.q.archived == True,
                                         orderBy=(DocumentDB.q.id, DocumentDB.q.path, DESC(DocumentDB.q.created)),
                                         start=offset, end=offset + limit,
                                         distinctOn=DocumentDB.q.id, distinct=True):

            documents.append({
                'id': document.id,
                'uuid': document.uuid,
                'name': document.name,
                'url': document.url,
                'type': document.type,
                'path': document.path,
                'created': str(document.created),
                'published': document.published
            })

        return Response(response=json.dumps({
            'documents': documents,
            'meta': {
                'offset': offset,
                'limit': limit
            }
        }), status=200, content_type='application/json')

    # pylint: disable=no-self-use
    @requires_permission('restore_deleted_document')
    def put(self, document_id=None):
        try:
            document = DocumentDB.restore_document(document_id)
            return Response(response=json.dumps({
                'notify_msg': {
                    'title': 'Restored',
                    'message': 'Document {0} has been restored'.format(str(document.name).strip()),
                    'type': 'success'
                }}), content_type='application/json', status=200)
        except DocumentNotFound:
            return Response(response=json.dumps({
                'notify_msg': {
                    'title': 'Cannot be found',
                    'message': 'Cannot find document to restore.',
                    'type': 'success'
                }}), content_type='application/json', status=404)

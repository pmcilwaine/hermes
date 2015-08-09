# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask.views import MethodView
from flask import request, Response, session
from hermes_cms.helpers import common
from sqlobject.sqlbuilder import DESC
from hermes_cms.core.registry import Registry
from hermes_cms.db import Document as DocumentDB
from hermes_cms.core.auth import requires_permission
from hermes_cms.validators import Document as DocumentValidation


class Document(MethodView):

    # pylint: disable=no-self-use
    @requires_permission('add_document')
    def post(self):
        document_data = request.json
        validation = DocumentValidation(data=document_data)
        if not validation.validate():
            return Response(response=json.dumps({
                'fields': validation.errors()
            }), status=400, content_type='application/json')

        if 'validate' in request.args:
            return Response(response=json.dumps(document_data), status=200, content_type='application/json')

        # todo we should use Auth class to get this
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

        return Response(response=json.dumps({}), status=200, content_type='application/json')

    # pylint: disable=no-self-use
    @requires_permission('modify_document')
    def put(self):
        pass

    # pylint: disable=no-self-use
    def get(self, document_id=None):
        def document_list():

            offset = int(request.args.get('offset', 0))
            limit = int(request.args.get('limit', 100))

            documents = []
            for document in DocumentDB.query(DocumentDB.all(), where=DocumentDB.q.archived == False,
                                             groupBy=(DocumentDB.q.id, DocumentDB.q.uuid, DocumentDB.q.created,
                                                      DocumentDB.q.published, DocumentDB.q.type, DocumentDB.q.name,
                                                      DocumentDB.q.archived, DocumentDB.q.menutitle,
                                                      DocumentDB.q.show_in_menu, DocumentDB.q.parent,
                                                      DocumentDB.q.path, DocumentDB.q.user_id),
                                             orderBy=DESC(DocumentDB.q.created), start=offset, end=offset + limit):

                documents.append({
                    'id': document.id,
                    'uuid': document.uuid,
                    'name': document.name,
                    'url': document.url,
                    'type': document.type
                })

            return Response(response=json.dumps({
                'documents': documents,
                'meta': {
                    'offset': offset,
                    'limit': limit
                }
            }), status=200, content_type='application/json')

        @requires_permission('modify_document')
        def document_get():
            record = DocumentDB.selectBy(uuid=document_id).getOne(None)
            if not record:
                # todo handle 404 requests correctly
                return Response(response=json.dumps({}), status=404, content_type='application/json')

            return Response(response=json.dumps(DocumentDB.get_document(record)), status=200,
                            content_type='application/json')

        if not document_id:
            return document_list()
        else:
            return document_get()

    # pylint: disable=no-self-use
    @requires_permission('delete_document')
    def delete(self, document_id):
        DocumentDB.delete_document(doc_uuid=document_id)
        return Response(status=200)

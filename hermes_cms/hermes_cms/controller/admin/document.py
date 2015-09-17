# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask.views import MethodView
from flask import request, Response, session
from hermes_cms.helpers import common
from sqlobject.sqlbuilder import DESC
from hermes_cms.core.registry import Registry
from hermes_cms.db import Document as DocumentDB
from hermes_cms.core.auth import Auth, requires_permission
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

        return Response(response=json.dumps({'notify_msg': {
            'title': 'Document Modified' if document_data.get('id') else 'Document Added',
            'message': '{0} has been {1}'.format(
                str(document.name).strip(),
                'modified' if document_data.get('id') else 'added'
            ),
            'type': 'success'
        }}), status=200, content_type='application/json')

    # pylint: disable=no-self-use,unused-argument
    @requires_permission('modify_document')
    def put(self, document_id=None):
        return self.post()

    def options(self):
        user = session.get('auth_user', {})
        option = {
            'POST': Auth.has_permission(user, 'add_document'),
            'PUT': Auth.has_permission(user, 'add_document,modify_document'),
            'DELETE': Auth.has_permission(user, 'delete_document')
        }

        if request.args.get('method'):
            if not option.get(request.args.get('method')):
                option['notify_msg'] = {
                    'title': 'No Permission',
                    'message': 'You do not have permission to perform that action',
                    'type': 'error'
                }

            return Response(
                response=json.dumps(option),
                status=403 if not option.get(request.args.get('method')) else 200,
                content_type='application/json')

        return Response(response=json.dumps(option), content_type='application/json', status=200)

    # pylint: disable=no-self-use,unused-argument
    def get(self, document_id=None):

        @requires_permission('list_document')
        def document_list():

            offset = int(request.args.get('offset', 0))
            limit = int(request.args.get('limit', 100))

            documents = []
            for document in DocumentDB.query(DocumentDB.all(), where=DocumentDB.q.archived == False,
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
                    'published': document.published
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

            content = DocumentDB.get_document(record)
            content['id'] = record.id

            return Response(response=json.dumps(content), status=200,
                            content_type='application/json')

        if not document_id:
            return document_list()
        else:
            return document_get()

    # pylint: disable=no-self-use
    @requires_permission('delete_document')
    def delete(self, document_id):
        DocumentDB.delete_document(doc_uuid=document_id)

        document = DocumentDB.selectBy(uuid=document_id).getOne(None)
        notification = {
            'title': 'Deleted',
            'message': '{0} has been deleted'.format(document.name.strip()),
            'type': 'success'
        }

        return Response(response=json.dumps({'notify_msg': notification}),
                        content_type='application/json',
                        status=200)

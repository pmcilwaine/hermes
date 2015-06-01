# /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from hermes_cms.core import Auth
from hermes_cms.views.exceptions import HermesRequestException, HermesNotSavedException
from hermes_cms.db import User, Document
from sqlobject.sqlbuilder import *
from hermes_cms.validators import User as UserValidation, Document as DocumentValidation
from flask import Blueprint, Response, request, json, session
from mako.lookup import TemplateLookup
from pkg_resources import resource_filename
from werkzeug.datastructures import MultiDict
from hermes_aws.s3 import S3
from hermes_cms.core.registry import Registry

log = logging.getLogger('hermes_cms.views.admin')
route = Blueprint('admin', __name__, url_prefix='/admin')
lookup = TemplateLookup(directories=[
    resource_filename('hermes_cms.templates.admin', '')
])


@route.route('/', methods=['GET'])
@Auth.is_logged_in
def index():
    return Response(response=lookup.get_template('index.html').render(), status=200)


@route.route('/user', methods=['GET'])
def user_get():

    users = []
    for user in User.selectBy(User.q.archived is False):
        users.append({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

    return Response(response=json.dumps({'users': users}), status=200, content_type='application/json')


@route.route('/user', methods=['POST'])
@route.route('/user/<user_id>', methods=['PUT'])
def user_post(user_id=None):
    try:
        if request.json is None:
            raise HermesRequestException('Invalid request was made')

        user_data = request.json
        user_data.pop('is_new', None)  # remove bad key
        if user_id:
            user_data['id'] = user_id

        validation = UserValidation(MultiDict(user_data))

        if not validation.validate():
            return Response(response=json.dumps({
                'fields': validation.errors()
            }), status=400, content_type='application/json')

        user = User.save(user_data)
        if not user:
            raise HermesNotSavedException('Unable to save user record')

        return Response(response=json.dumps({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }), status=200, content_type='application/json')

    except (HermesRequestException, HermesNotSavedException) as e:
        return Response(response=e.as_json(), status=400, content_type='application/json')


@route.route('/user/<user_id>', methods=['DELETE'])
def user_delete(user_id=None):
    return Response(status=200)


@route.route('/document', methods=['GET'])
def document_list():

    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 100))

    documents = []
    for document in Document.query(Document.all(), where=Document.q.archived == False, groupBy=Document.q.url,
                                   orderBy=DESC(Document.q.created), start=offset, end=offset + limit):

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


@route.route('/document/<uuid>', methods=['GET'])
def document_get(uuid=None):
    record = Document.selectBy(uuid=uuid).getOne(None)
    if not record:
        # todo handle 404 requests correctly
        return Response(response=json.dumps({}), status=404, content_type='application/json')

    return Response(response=json.dumps(Document.get_document(record)), status=200,
                    content_type='application/json')


@route.route('/document/<uuid>', methods=['DELETE'])
def document_delete(uuid=None):
    Document.delete_document(doc_uuid=uuid)
    return Response(status=200)


@route.route('/document', methods=['POST'])
def document_add():

    document_data = request.json
    validation = DocumentValidation(data=document_data)
    if not validation.validate():
        return Response(response=json.dumps({
            'fields': validation.errors()
        }), status=400, content_type='application/json')

    if 'validate' in request.args:
        return Response(response=json.dumps(document_data), status=200, content_type='application/json')

    # todo we should use Auth class to get this
    document_data['document']['user'] = session['auth_user'].get('id', -1)
    document = Document.save(document_data)
    return Response(response=json.dumps({}), status=200, content_type='application/json')


@route.route('/upload_url', methods=['POST'])
def sign_upload_url():

    bucket = Registry().get('files')['bucket_name']
    signed_form = S3.generate_form(bucket)
    signed_form['file'] = {
        'bucket': bucket,
        'key': [item['value'] for item in signed_form['fields'] if item['name'] == 'key'].pop()
    }

    return Response(response=json.dumps(signed_form), content_type='application/json', status=201)

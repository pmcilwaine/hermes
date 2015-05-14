# /usr/bin/env python
# -*- coding: utf-8 -*-

from hermes_cms.core import Auth
from hermes_cms.views.exceptions import HermesRequestException, HermesNotSavedException
from hermes_cms.db import User
from hermes_cms.validators import User as UserValidation
from flask import Blueprint, Response, request, json
from mako.lookup import TemplateLookup
from pkg_resources import resource_filename
from werkzeug.datastructures import MultiDict

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
            'uid': user.uid,
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
            user_data['uid'] = user_id

        validation = UserValidation(MultiDict(user_data))

        if not validation.validate():
            return Response(response=json.dumps({
                'fields': validation.errors()
            }), status=400, content_type='application/json')

        user = User.save(user_data)
        if not user:
            raise HermesNotSavedException('Unable to save user record')

        return Response(response=json.dumps({
            'uid': user.uid,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }), status=200, content_type='application/json')

    except (HermesRequestException, HermesNotSavedException) as e:
        return Response(response=e.as_json(), status=400, content_type='application/json')


@route.route('/user/<user_id>', methods=['DELETE'])
def user_delete(user_id=None):
    return Response(status=200)

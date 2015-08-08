# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask.views import MethodView
from flask import request, Response
from hermes_cms.core.auth import requires_permission
from hermes_cms.db import User as UserDB
from werkzeug.datastructures import MultiDict
from hermes_cms.validators import User as UserValidation
from hermes_cms.views.exceptions import HermesRequestException, HermesNotSavedException


class User(MethodView):

    # pylint: disable=no-self-use
    @requires_permission('add_user')
    def post(self):
        return User._handle_submission()

    # pylint: disable=no-self-use
    @requires_permission('modify_user')
    def put(self, user_id):
        return User._handle_submission(user_id)

    @staticmethod
    def _handle_submission(user_id=None):
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

            user_data['first_name'] = user_data.get('first_name', '')
            user_data['last_name'] = user_data.get('last_name', '')

            user = UserDB.save(user_data)
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

    # pylint: disable=no-self-use
    def get(self, user_id=None):
        def _get_all_users():
            users = []
            for user in UserDB.selectBy(UserDB.q.archived is False):
                users.append({
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                })

            return Response(response=json.dumps({'users': users}), status=200, content_type='application/json')

        @requires_permission('modify_user')
        def _get_single_user():
            user = UserDB.selectBy(id=user_id).getOne(None)
            if not user:
                return Response(status=404)

            return Response(response=json.dumps({
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'permissions': user.permissions
            }), status=200, content_type='application/json')

        if not user_id:
            return _get_all_users()
        else:
            return _get_single_user()

    # pylint: disable=no-self-use
    @requires_permission('delete_user')
    def delete(self, user_id):
        return Response(status=200)

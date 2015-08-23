# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask.views import MethodView
from flask import Response
from hermes_cms.db import User as UserDB
from hermes_cms.core.auth import requires_permission


class RestoreUser(MethodView):

    # pylint: disable=no-self-use
    @requires_permission('restore_user')
    def get(self):
        users = []
        for user in UserDB.selectBy(archived=True):
            users.append({
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            })

        return Response(response=json.dumps({'users': users}), status=200, content_type='application/json')

    # pylint: disable=no-self-use
    @requires_permission('restore_user')
    def put(self, user_id=None):
        user = UserDB.selectBy(id=user_id).getOne(None)
        if not user:
            return Response(response=json.dumps({
                'notify_msg': {
                    'title': 'Not Found',
                    'message': 'Could not find user to restore.',
                    'type': 'success'
                }}), content_type='application/json', status=404)

        user.set(archived=False)

        return Response(response=json.dumps({
            'notify_msg': {
                'title': 'User Restored',
                'message': 'User {0} has been restored'.format(str(user.email).strip()),
                'type': 'success'
            }}), content_type='application/json', status=200)

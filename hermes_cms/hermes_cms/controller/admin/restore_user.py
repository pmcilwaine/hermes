# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask.views import MethodView
from flask import request, Response
from hermes_cms.db import User as UserDB
from hermes_cms.core.auth import requires_permission


class RestoreUser(MethodView):

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

    @requires_permission('restore_user')
    def put(self, user_id=None):
        user = UserDB.selectBy(id=user_id).getOne(None)
        if not user:
            return Response(status=404)

        user.set(archived=False)

        return Response(status=200)

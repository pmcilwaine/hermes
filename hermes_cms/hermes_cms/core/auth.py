# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib
from functools import wraps
from flask import session, redirect, request, Response
from hermes_cms.db import User


class Auth(object):

    @staticmethod
    def get_by_login(email, password):
        """
        Finds out if the user is valid by checking the email and password supplied.

        @param email: The email address to use.
        @param password: The password as plaintext to use.
        @return User|None
        """
        return User.selectBy(email=email, password=User.hash_password(password)).getOne(None)

    @staticmethod
    def create_session(user):
        """
        Create a session if the user object is valid.

        @param user A `hermes_cms.db.User` object
        """
        if user:
            session['auth_user'] = user.as_json()

    @staticmethod
    def delete_session():
        if 'auth_user' in session:
            session.pop('auth_user')
            return True

        return False

    @staticmethod
    def is_logged_in(func):
        @wraps(func)
        def _is_logged(*args, **kwargs):
            if session.get('auth_user', None):
                return func(*args, **kwargs)
            else:
                return redirect('/login?next_page={0}'.format(urllib.quote_plus(request.full_path)))

        return _is_logged

    @staticmethod
    def has_permission(user, permissions):
        """
        Check if the user has permissions to use a resource.

        Returns True if they do and False otherwise. No error message is supplied and it is up to the callee
         to show an error message if has_permission returns False

        @param user: The `dict` stored as the auth_user in the session object
        @param permissions: a `list` or `str` of permissions to check for. String can only be used for a single
        permission
        @return True if the user has permission and False if user does not have permission
        """

        if isinstance(permissions, basestring):
            permissions = {permissions}
        else:
            permissions = set(permissions)

        # if there is no difference than we have all required permissions
        return not permissions.difference(set(user.get('permissions', [])))

    @staticmethod
    def requires_permission(permissions):

        def _decorator(func):
            @wraps(func)
            def _has_permission(*args, **kwargs):
                user = session.get('auth_user', {})
                if Auth.has_permission(user, permissions):
                    return func(*args, **kwargs)
                else:
                    return Response(response=json.dumps({
                        'notify_msg': {
                            'title': 'No Permission',
                            'message': 'You do not have permission to perform that action',
                            'type': 'error'
                        }
                    }), status=403, content_type='application/json')

            return _has_permission

        return _decorator

requires_permission = Auth.requires_permission

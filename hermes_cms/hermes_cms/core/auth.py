# /usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from flask import session, redirect
from hermes_cms.db import User


class Auth(object):

    @staticmethod
    def get_by_login(email, password):
        """
        Finds out if the user is valid by checking the email and password supplied.

        :param email: The email address to use.
        :type email: basestring
        :param password: The password as plaintext to use.
        :type password: basestring
        :rtype: User|None
        """
        return User.selectBy(email=email, password=User.hash_password(password)).getOne(None)

    @staticmethod
    def create_session(user):
        """

        :type user: hermes_cms.db.User
        :param user:
        :return:
        """
        if user:
            session['auth_user'] = user.as_json()

    @staticmethod
    def is_logged_in(func):
        @wraps(func)
        def _is_logged(*args, **kwargs):
            if session.get('auth_user', None):
                return func(*args, **kwargs)
            else:
                return redirect('/login')

        return _is_logged

    @staticmethod
    def has_permission(user, permissions):
        """
        Check if the user has permissions to use a resource.

        Returns True if they do and False otherwise. No error message is supplied and it is up to the callee
         to show an error message if has_permission returns False

        :type user: dict
        :param user: The dictionary stored as the auth_user in the session object
        :type permissions: basestring|list
        :param permissions: a list or string of permissions to check for. String can only be used for a single
        permission
        :rtype: bool
        """

        if isinstance(permissions, basestring):
            permissions = {permissions}
        else:
            permissions = set(permissions)

        # if there is no difference than we have all required permissions
        return not permissions.difference(set(user.get('permissions', [])))

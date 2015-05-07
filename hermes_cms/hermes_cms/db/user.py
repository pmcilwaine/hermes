# /usr/bin/env python
# -*- coding: utf-8 -*-

from sqlobject import SQLObject, StringCol, PickleCol, DateTimeCol, BoolCol
import hashlib

__all__ = ['User']


class User(SQLObject):
    email = StringCol(length=255, alternateID=True)
    password = StringCol(length=64)
    first_name = StringCol(length=255)
    last_name = StringCol(length=255)
    created = DateTimeCol().now()
    modified = DateTimeCol().now()
    archived = BoolCol(default=False)
    permissions = PickleCol(default=set())

    def _set_password(self, value):
        self._SO_set_password(User.hash_password(value))

    @staticmethod
    def hash_password(password):
        """
        This creates a sha 256 hash of the password to store and use for login.

        :type password: basestring
        :param password:
        :return: str
        """
        h = hashlib.sha256()
        h.update(password)
        return h.hexdigest()

    def as_json(self):
        """

        :return: dict
        """
        return {'email': self.email, 'permissions': list(self.permissions)}

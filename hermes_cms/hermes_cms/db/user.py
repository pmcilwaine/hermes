# /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlobject import SQLObject
from sqlobject.col import StringCol, DateTimeCol, BoolCol
import hashlib

__all__ = ['User']


class User(SQLObject):

    class sqlmeta(object):
        table = "users"

    email = StringCol(length=255)
    password = StringCol(length=64)
    first_name = StringCol(length=255)
    last_name = StringCol(length=255)
    created = DateTimeCol(default=datetime.now())
    modified = DateTimeCol(default=datetime.now())
    archived = BoolCol(default=False)
    permissions = StringCol(default='')

    def _set_password(self, value):
        # pylint: disable=no-member
        self._SO_set_password(User.hash_password(value))

    def _get_permissions(self):
        # pylint: disable=no-member
        return self._SO_get_permissions().split(',')

    def _set_permissions(self, value):
        if isinstance(value, (tuple, list)):
            value = ','.join(value)

        self._SO_set_permissions(value)

    @staticmethod
    def hash_password(password):
        """
        This creates a sha 256 hash of the password to store and use for login.

        :type password: basestring
        :param password:
        :return: str
        """
        value = hashlib.sha256()
        value.update(password)
        return value.hexdigest()

    @staticmethod
    def save(record):
        """

        :type record: dict
        :param record:
        :return:
        """
        if 'id' not in record:
            user = User(**record)
        else:
            user = User.selectBy(email=record['email']).getOne(None)
            if not user:
                # todo better exception handling here
                raise Exception('Cannot find user record to update')
            record.pop('id')  # todo find out how we can force id to be par of the kwargs
            user.set(**record)

        return user

    def as_json(self):
        """

        :return: dict
        """
        return {'id': self.id, 'email': self.email, 'permissions': self.permissions}

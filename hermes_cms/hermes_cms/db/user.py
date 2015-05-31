# /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlobject import SQLObject
from sqlobject.col import StringCol, PickleCol, DateTimeCol, BoolCol
import hashlib
import uuid

__all__ = ['User']


class User(SQLObject):
    email = StringCol(length=255)
    password = StringCol(length=64)
    first_name = StringCol(length=255)
    last_name = StringCol(length=255)
    created = DateTimeCol(default=datetime.now())
    modified = DateTimeCol(default=datetime.now())
    archived = BoolCol(default=False)
    permissions = PickleCol(default=set())

    def _set_password(self, value):
        # pylint: disable=no-member
        self._SO_set_password(User.hash_password(value))

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
            user = User.selectBy(email=record['email'])
            user.set(**record)

        return user

    def as_json(self):
        """

        :return: dict
        """
        return {'id': self.id, 'email': self.email, 'permissions': list(self.permissions)}

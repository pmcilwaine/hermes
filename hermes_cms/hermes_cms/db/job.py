# /usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import json
from sqlobject import SQLObject
from sqlobject.col import StringCol, DateTimeCol


class Job(SQLObject):
    uuid = StringCol(length=36)
    name = StringCol(length=255)
    status = StringCol(length=8)
    created = DateTimeCol(default=DateTimeCol.now())
    modified = DateTimeCol(default=DateTimeCol.now())
    message = StringCol()

    def _get_name(self):
        # pylint: disable=no-member
        return str(self._SO_get_name()).strip()

    def _get_message(self):
        # pylint: disable=no-member
        return json.loads(self._SO_get_message())

    def _set_message(self, value):
        # pylint: disable=no-member
        self._SO_set_message(json.dumps(value))

    @staticmethod
    def save(record):
        """

        :type record: dict
        :param record:
        :return:
        """
        if 'uuid' not in record:
            record['uuid'] = str(uuid.uuid4())
            job = Job(**record)
        else:
            job = Job.selectBy(uuid=record['uuid']).getOne(None)

            if not job:
                # todo better exception handling here
                raise Exception('Cannot find job record to update')

            job.pop('uuid')
            job.set(**record)

        return job

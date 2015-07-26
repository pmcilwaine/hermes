# /usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
from datetime import datetime
from sqlobject import SQLObject
from sqlobject.col import StringCol, DateTimeCol, PickleCol


class Job(SQLObject):
    uuid = StringCol(length=64)
    name = StringCol(length=255)
    status = StringCol(length=8)
    created = DateTimeCol(default=datetime.now())
    modified = DateTimeCol(default=datetime.now())
    message = PickleCol(default={})

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

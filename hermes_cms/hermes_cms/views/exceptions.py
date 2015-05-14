# /usr/bin/env python
# -*- coding: utf-8 -*-
import json


class HermesBaseException(Exception):

    title = None

    def as_json(self):
        return json.dumps({
            'title': self.title,
            'message': self.message
        })


class HermesRequestException(HermesBaseException):
    title = 'Invalid Request'


class HermesNotSavedException(HermesBaseException):
    pass

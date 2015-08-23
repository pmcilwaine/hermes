# /usr/bin/env python
# -*- coding: utf-8 -*-


class Document(object):
    """
    The base object for normal display of documents. All document types
    must extend this class.
    """

    def __init__(self, document, config):
        self._document = document
        self._config = config

    def get(self):
        raise NotImplementedError('This method has not been implemented')

    def post(self):
        raise NotImplementedError('This method has not been implemented')

    def put(self):
        raise NotImplementedError('This method has not been implemented')

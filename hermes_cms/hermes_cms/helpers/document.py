# /usr/bin/env python
# -*- coding: utf-8 -*-


class DocumentHelper(object):

    def __init__(self, document):
        self.document = document

    def do_work(self):
        raise NotImplementedError('This method must be overridden')

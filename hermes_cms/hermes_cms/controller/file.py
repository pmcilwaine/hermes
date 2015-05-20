# /usr/bin/env python
# -*- coding: utf-8 -*-

from hermes_cms.controller.document import Document
from flask import Response


class File(Document):

    def get(self):
        return {
            'file': {
                'filename': '',
                'content_type': '',
                's3': {
                    'bucket_name': '',
                    'key_name': ''
                }
            }
        }

    def put(self):
        pass

    def post(self):
        pass

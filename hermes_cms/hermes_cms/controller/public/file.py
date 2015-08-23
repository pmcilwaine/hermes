# /usr/bin/env python
# -*- coding: utf-8 -*-

from hermes_cms.controller.public.document import Document
from hermes_aws.s3 import S3
from flask import Response


class File(Document):
    """
    The File Type Document controller. It only allows GET requests
    """

    def get(self):
        generator = S3.stream_file(self._document['file']['bucket'], self._document['file']['key'])
        return Response(generator, status=200, mimetype=self._document['file']['type'], headers={
            'Content-Disposition': 'attachment; filename={0}'.format(self._document['file']['name'])
        })

    def put(self):
        pass

    def post(self):
        pass

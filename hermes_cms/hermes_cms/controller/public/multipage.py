# /usr/bin/env python
# -*- coding: utf-8 -*-
from hermes_cms.controller.public import Document
from hermes_cms.core.registry import Registry
from hermes_aws import S3
from flask import request, Response


class Multipage(Document):
    def get(self):
        registry = Registry()

        (_, key_name) = request.path.split('/{0}'.format(self._document['document']['url']))
        if '/' == key_name:
            key_name = '/index.html'  # todo must have a default start page for multipage

        key_name = '{0}{1}'.format(self._document['document']['uuid'], key_name)
        generator = S3.stream_file(registry.get('files').get('bucket_name'), key_name)

        # todo we need to get the mimetype of the actual key some how.
        return Response(generator, status=200,
                        mimetype=S3.get_content_type(registry.get('files').get('bucket_name'), key_name))

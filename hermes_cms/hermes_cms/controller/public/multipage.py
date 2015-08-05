# /usr/bin/env python
# -*- coding: utf-8 -*-
from hermes_cms.controller.public.document import Document
from hermes_cms.core.registry import Registry
from hermes_aws import S3
from flask import request, Response


# pylint: disable=abstract-method
class Multipage(Document):

    def get(self):
        registry = Registry()

        (_, key_name) = request.path.split('/{0}'.format(self._document['document']['url']))
        if not key_name or '/' == key_name:
            key_name = '/index.html'  # todo must have a default start page for multipage

        key_name = '{0}{1}'.format(self._document['document']['uuid'], key_name)
        contents = S3.get_string(registry.get('files').get('bucket_name'), key_name)

        # todo we need to get the mimetype of the actual key some how.
        return Response(response=contents, status=200,
                        mimetype=S3.get_content_type(registry.get('files').get('bucket_name'), key_name))

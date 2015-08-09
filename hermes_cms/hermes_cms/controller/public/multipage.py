# /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import mimetypes
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

        tmp_dir = os.path.abspath(os.path.join('/tmp/multipage', self._document['document']['uuid']))
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        file_path = os.path.abspath(os.path.join(tmp_dir, key_name[1:]))
        if os.path.exists(file_path):
            with open(file_path, 'r') as content:
                contents = content.read()
        else:
            key_name = '{0}{1}'.format(self._document['document']['uuid'], key_name)
            contents = S3.get_string(registry.get('files').get('bucket_name'), key_name)

            dir_name = os.path.dirname(file_path)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            with open(file_path, 'w') as write:
                write.write(contents)

        mimetype = mimetypes.guess_type(file_path)[0]
        return Response(response=contents, status=200, mimetype=mimetype)

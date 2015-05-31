# /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from hermes_cms.db import Document
from sqlobject.sqlbuilder import IN
from flask import Response, request

log = logging.getLogger('hermes_cms.core.route')


# todo this registry should be removed later. for Prototype purposes we keep this hardcoded.
REGISTRY = {
    'type': [
        'Page',
        'File'
    ],
    'Page': {
        'templates': {
            'Homepage': 'index.html',
            'Standard': 'standard-page.html'
        },
        'template_modules': [
            'hermes_cms.templates.public'
        ],
        'document_module': 'hermes_cms.controller',
        'document_class': 'Page'
    },
    'File': {
        'document_module': 'hermes_cms.controller',
        'document_class': 'File'
    },
    'Error': {
        'document_module': 'hermes_cms.controller',
        'document_class': 'Error'
    }
}


def route(path):
    """

    :type path: str
    :param path:
    :return:
    :rtype: Response
    """

    urls = [path]
    tmp_str = str(path)
    while tmp_str != '':
        tmp_str = '/'.join(tmp_str.split('/')[0:-1])
        if tmp_str:
            urls.append(tmp_str)

    log.debug('Attempting to get urls %s' % (urls, ))
    record = Document.select(IN(Document.q.url, urls)).getOne(None)
    if not record:
        return Response(status=404)

    document = Document.get_document(record)

    registry_type = REGISTRY[record.type]
    controller = getattr(__import__(registry_type['document_module'], fromlist=registry_type['document_class']),
                         registry_type['document_class'])

    record_controller = controller(document, registry_type)
    return getattr(record_controller, str(request.method).lower())()

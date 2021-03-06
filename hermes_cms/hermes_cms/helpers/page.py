# /usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import logging
from hermes_cms.db import Document
from mako.runtime import Undefined
from sqlobject.sqlbuilder import DESC, LIKE

log = logging.getLogger('hermes_cms.helpers.page')
NAVIGATION_ALL = 'all'
NAVIGATION_CURRENT_DEPTH = 'current_depth'
NAVIGATION_CHILDREN = 'children'


def navigation(document, depth=None):
    """
    Builds a navigation data structure that can be used to show navigation on a Page Type.

    :type document: dict
    :param document: A dictionary object that is stored in S3
    :param depth: Valid values of 'all' and 'current_depth' all will show every single page. 'current_depth' will only
                    get documents within the current tree depth
    :return: dict
    :rtype: dict
    """

    if depth not in [NAVIGATION_ALL, NAVIGATION_CURRENT_DEPTH]:
        pass

    # depth = depth or NAVIGATION_ALL

    query = ((Document.q.archived == False) & (Document.q.show_in_menu == True) &
             (Document.q.published == True))

    if depth == NAVIGATION_CHILDREN and (document and not isinstance(document['document'], Undefined)):
        query &= (LIKE(Document.q.path, '{0}%'.format(document['document']['path'])))

    results = []
    parent = {}

    for page in Document.query(Document.all(), where=query,
                               orderBy=(Document.q.id, Document.q.path, DESC(Document.q.created)),
                               distinctOn=Document.q.id, distinct=True):

        current = False
        if document and not isinstance(document['document'], Undefined):
            current = document['document']['path'].startswith(page.path)

        record = {
            'url': '/' if page.url == 'index' else '/' + page.url,
            'menutitle': cgi.escape(page.menutitle),
            'current': current,
            'children': []
        }

        parent.update({page.id: record})
        if page.parent in parent:
            parent[page.parent]['children'].append(record)
        else:
            results.append(record)

    return results

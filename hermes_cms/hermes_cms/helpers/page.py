# /usr/bin/env python
# -*- coding: utf-8 -*-

from hermes_cms.db import Document

NAVIGATION_ALL = 'all'
NAVIGATION_CURRENT_DEPTH = 'current_depth'


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

    query = ((Document.q.archived == True) & (Document.q.show_in_menu == True) &
             (Document.q.published == True))

    results = []
    parent = {}
    for page in Document.selectBy(query):

        record = {
            'url': page.url,
            'menutitle': page.menutitle,
            'current': document['document']['path'].startswith(page.path),
            'children': []
        }

        parent.update({page.gid: record})
        if page.parent in parent:
            parent[page.parent]['children'].append(record)
        else:
            results.append(record)

    return results
# /usr/bin/env python
# -*- coding: utf-8 -*-


class Registry(object):

    def get(self, name):
        return [{
            'name': 'hermes_cms.views.main', 'from': 'route'
        }, {
            'name': 'hermes_cms.views.admin', 'from': 'route'
        }]

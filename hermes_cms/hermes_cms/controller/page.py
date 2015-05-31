# /usr/bin/env python
# -*- coding: utf-8 -*-

from hermes_cms.controller.document import Document
from hermes_cms.helpers.page import navigation, NAVIGATION_CURRENT_DEPTH
from flask import Response
from mako.lookup import TemplateLookup
from pkg_resources import resource_filename


class Page(Document):

    def __init__(self, document, config):
        super(Page, self).__init__(document, config)

        templates = [resource_filename(template, '') for template in config.get('template_modules', [])]
        self.lookup = TemplateLookup(templates)

    def get(self):
        template = self.lookup.get_template(self._config['templates'][self._document['page']['template']])
        print navigation(self._document, NAVIGATION_CURRENT_DEPTH)
        return Response(response=template.render(**self._document),
                        status=200, content_type='text/html')

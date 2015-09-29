# /usr/bin/env python
# -*- coding: utf-8 -*-

from hermes_cms.controller.public.document import Document
from hermes_cms.helpers.page import navigation
from flask import Response, session
from mako.lookup import TemplateLookup
from pkg_resources import resource_filename


class Page(Document):
    """
    The Page Type Document. It only allows GET requests.
    """

    def put(self):
        pass

    def post(self):
        pass

    def __init__(self, document, config):
        super(Page, self).__init__(document, config)

        templates = [resource_filename(template, '') for template in config.get('template_modules', [])]
        self.lookup = TemplateLookup(templates)

    def get(self):
        template = self.lookup.get_template(self._config['templates'][self._document['page']['template']])
        return Response(response=template.render(**dict(nav=navigation, is_logged_in=('auth_user' in session),
                                                        **self._document)),
                        status=200, content_type='text/html')

# /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Response
from mako.lookup import TemplateLookup
from pkg_resources import resource_filename
from hermes_cms.helpers.page import navigation
from hermes_cms.controller.public.document import Document


class Error(Document):

    def __init__(self, document, config):
        super(Error, self).__init__(document, config)

        templates = [resource_filename(template, '') for template in config.get('template_modules', [])]
        self.lookup = TemplateLookup(templates)

    def put(self):
        pass

    def post(self):
        pass

    def get(self):
        template = self.lookup.get_template(self._config['templates'][str(self._document.get('status'))])
        return Response(response=template.render(**dict(nav=navigation, **self._document)),
                        status=self._document.get('status', 404), content_type='text/html')

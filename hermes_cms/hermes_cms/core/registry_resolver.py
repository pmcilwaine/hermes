# /usr/bin/env python
# -*- coding: utf-8 -*-
from hermes_cms.core.registry import Registry
from urlparse import urlparse


class RegistryResolver(object):

    def __init__(self):
        self.registry = Registry()

    def _get_dict(self, dict_src, path):
        """

        :param dict_src:
        :param path:
        :return:
        """
        dict_dest = dict_src
        for item in path.split('.'):
            dict_dest = dict_dest[item]

        return dict_dest

    def _resolve_string(self, value):
        """

        :type value: basestring
        :param value: A string to be parsed from a registry.
        :return:
        """
        parsed_path = urlparse(value)
        if not parsed_path.scheme:
            return value

        full_path = parsed_path.path.lstrip('/')
        (bucket, path) = full_path.split('.', 1)
        resolved_config = self.registry.get(bucket)
        return self._get_dict(resolved_config, path)

    def resolver(self, value):
        """

        :param value:
        :return:
        """
        if isinstance(value, basestring):
            return self._resolve_string(value)

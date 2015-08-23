# /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import logging
# todo aws stuff should be moved into hermes_aws package
import boto
from boto.s3.key import Key


class Registry(object):

    BUCKET_NAME = '/etc/sysconfig/config-bucket'
    CACHE = '/tmp/config'

    def __init__(self, log=None):
        """

        @param log A python logging object
        """
        self._log = log or logging.getLogger('hermes_cms.core.registry.Registry')
        self._bucket_name_ = None
        self._cache = {}
        if not os.path.exists(Registry.CACHE):
            self._log.debug('Creating Registry Cache directory')
            os.makedirs(Registry.CACHE)

    def get(self, key):
        """
        Get the registry configuration from the S3 configuration bucket

        @param key The name of the registry key file to retrieve
        @return A dictionary which maybe empty as the file was not found.
        """
        value = self._read_key(key)

        try:
            self._log.debug("Registry.get('%s') returns %s" % (key, value))
            return json.loads(value)
        except (TypeError, ValueError) as e:
            self._log.error('Unable to parse registry file %s from %s [%s]', key, value, str(e))

        return {}

    def _read_cache(self, key):
        """
        Read the key stored in cache otherwise return None

        @param key The name of the registry key file to retrieve
        @return None if we cannot find the key in the cache.
        """
        if key in self._cache:
            return self._cache[key]

        try:
            with open(os.path.join(Registry.CACHE, key), 'r') as config:
                self._cache[key] = config.read().strip()
                return self._cache[key]
        except IOError as e:
            self._log.error('Unable to read key registry file %s [%s]' % (key, str(e)))

        return None

    def _write_key(self, key, value):
        """

        @param key The name of file in s3 storage
        @param value The string value retrieved from s3 storage
        @return: No value returned
        """
        try:
            value = value.strip()
            with open(os.path.join(Registry.CACHE, key), 'w') as cache:
                cache.write(value)
                self._cache[key] = value
        except IOError as e:
            self._log.error('Unable to save registry %s to cache [%s]' % (key, str(e)))

    def _read_key(self, key):
        """

        @param key The name of the registry key file to retrieve
        @return basestring | None
        """
        value = self._read_cache(key)
        if value is not None:
            return value

        value = self._get_s3(key)
        self._write_key(key, value)
        return value

    def _get_s3(self, resource):
        """

        @param resource The name of the resource to retrieve
        @return No return value
        """
        conn = boto.connect_s3()
        bucket = conn.get_bucket(self._bucket_name)
        key = Key(bucket)
        key.name = resource
        value = key.get_contents_as_string()
        return value.strip()

    @property
    def _bucket_name(self):
        if not self._bucket_name_:
            self._log.info('opening %s to read from bucket' % (Registry.BUCKET_NAME, ))

            try:
                with open(Registry.BUCKET_NAME, 'r') as registry:
                    self._bucket_name_ = registry.read().strip()
                    self._log.info('using bucket %s for registry' % (self._bucket_name_, ))
            except IOError as e:
                self._log.error('Failed to read from bucket file %s [%s]' % (Registry.BUCKET_NAME, str(e)))

        return self._bucket_name_

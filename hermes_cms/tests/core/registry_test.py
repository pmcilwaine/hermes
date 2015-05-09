# /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from moto import mock_s3
from boto.s3 import connection
from mock import patch, PropertyMock, mock_open
from hermes_cms.core.registry import Registry


def test_registry_bucket_file():
    assert "/etc/sysconfig/config-bucket" == Registry.BUCKET_NAME


@mock_s3
def test_registry_region():
    expected = 'my region'
    bucket_name = 'my-bucket'

    s3 = connection.S3Connection()
    bucket = s3.create_bucket(bucket_name)
    key = bucket.new_key('region')
    key.set_contents_from_string('{"region": "%s"}' % (expected, ))

    with patch('hermes_cms.core.registry.Registry._bucket_name', new_callable=PropertyMock) as mock_bucket_name:
        mock_bucket_name.return_value = bucket_name
        registry = Registry()
        assert registry.get('region').get('region') == expected


def test_registry_region_cached(caplog):
    expected = 'my region'
    caplog.setLevel(logging.DEBUG)
    with patch('hermes_cms.core.registry.open', mock_open(read_data='{"region": "%s"}' % (expected, )), create=True):
        registry = Registry()
        assert registry.get('region').get('region') == expected

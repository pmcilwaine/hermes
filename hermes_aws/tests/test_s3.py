# /usr/bin/env python
# -*- coding: utf-8 -*-
import boto
import arrow
from mock import patch
from moto import mock_s3
from boto.s3.key import Key
from hermes_aws.s3 import S3


@mock_s3
@patch('hermes_aws.s3.arrow')
def test_upload_string(arrow_mock):
    conn = boto.connect_s3()
    conn.create_bucket('source-bucket')

    mocked_date = arrow.get('2015-01-1')
    arrow_mock.utcnow.return_value = mocked_date

    the_date = mocked_date.date()
    expected = '%s/%s/%s/%s' % (the_date.day, the_date.month, the_date.year, 'test-name')
    assert expected == S3.upload_string('source-bucket', 'test-name', 'my string')


@mock_s3
def test_upload_string_no_partition():
    conn = boto.connect_s3()
    conn.create_bucket('source-bucket')

    assert 'test-name' == S3.upload_string('source-bucket', 'test-name', 'my string', partition=False)


@mock_s3
def test_get_string():
    conn = boto.connect_s3()
    conn.create_bucket('source-bucket')
    bucket = conn.get_bucket('source-bucket')

    key = Key(bucket=bucket, name='the-file')
    key.set_contents_from_string('the string')

    assert 'the string' == S3.get_string('source-bucket', 'the-file')


@mock_s3
@patch('hermes_aws.s3.uuid')
@patch('hermes_aws.s3.arrow')
def test_generate_form(arrow_mock, uuid_mock):
    conn = boto.connect_s3()
    conn.create_bucket('source-bucket')

    uuid_mock.uuid4.return_value = 'test-id'

    mocked_date = arrow.get('2015-01-1')
    arrow_mock.utcnow.return_value = mocked_date

    the_date = mocked_date.date()
    expected_keyname = '%s/%s/%s/%s' % (the_date.day, the_date.month, the_date.year, 'test-id')

    response = S3.generate_form('source-bucket')
    assert response['action'] == 'https://source-bucket.s3.amazonaws.com/'
    assert [item for item in response['fields'] if item['name'] == 'key'][0]['value'] == expected_keyname

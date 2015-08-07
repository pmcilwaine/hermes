# /usr/bin/env python
# -*- coding: utf-8 -*-
import boto
import arrow
import uuid
from boto.exception import S3ResponseError
from boto.s3.key import Key


class S3Error(Exception):
    pass


class S3(object):

    def __init__(self):
        self.conn = boto.connect_s3()

    def metadata(self, bucket_name, key_name):
        """

        :type bucket_name: basestring
        :param bucket_name: The name of the bucket
        :type key_name: basestring
        :param key_name: The name of the key in the bucket
        :return: dict
        """
        bucket = self.conn.get_bucket(bucket_name)
        key = bucket.get_key(key_name)
        if not key:
            raise S3Error('Key does not exist')

        return {
            'Content-Type': key.content_type
        }

    @staticmethod
    def upload_string(bucket_name, key_name, contents, partition=True, bucket=None):
        """

        :param bucket_name:
        :param key_name:
        :param contents:
        :return:
        """
        if not bucket:
            connection = boto.connect_s3()
            bucket = connection.get_bucket(bucket_name)

        if partition:
            date = arrow.utcnow().date()
            key_name = '%s/%s/%s/%s' % (date.day, date.month, date.year, key_name)

        key = Key(bucket=bucket, name=key_name)
        key.set_contents_from_string(contents)

        return key.name

    @staticmethod
    def get_string(bucket_name, key_name):
        connection = boto.connect_s3()
        bucket = connection.get_bucket(bucket_name)
        key = Key(bucket=bucket, name=key_name)
        return key.get_contents_as_string()

    @staticmethod
    def generate_form(bucket_name, expires_in=None, key_name=None, region=None, acl='private'):
        """
        Generates what is required for a form to post directly to S3 bucket.

        :param bucket_name:
        :param expires_in:
        :param key_name:
        :param acl:
        :return: Returns a dictionary ready to send to the client to produce a Form.
        :rtype: dict
        """
        if not key_name:
            date = arrow.utcnow().date()
            key_name = "{0}/{1}/{2}/{3}".format(date.day, date.month, date.year, uuid.uuid4())

        if not expires_in:
            expires_in = 3600

        fields = [{
            'name': 'success_action_status',
            'value': '201'
        }]

        conditions = ["{'success_action_status': '201'}"]

        if region:
            connection = boto.s3.connect_to_region(region)
        else:
            connection = boto.connect_s3()

        response = connection.build_post_form_args(bucket_name, key_name, expires_in=expires_in, acl=acl,
                                                   fields=fields, http_method='https', conditions=conditions)

        return response

    @staticmethod
    def generate_download_url(bucket, key_name, region='ap-southeast-2'):
        """

        :param bucket:
        :param key_name:
        :param region:
        :return:
        :rtype: str
        """
        if region:
            connection = boto.s3.connect_to_region(region)
        else:
            connection = boto.connect_s3()

        try:
            bucket = connection.get_bucket(bucket)
        except S3ResponseError:
            raise KeyError('Invalid Bucket Name')

        key = bucket.get_key(key_name)
        if not key:
            raise KeyError('Invalid Key name for bucket')

        return key.generate_url(expires_in=300, method='GET')

    @staticmethod
    def get_content_type(bucket_name, key_name):
        connection = boto.connect_s3()
        bucket = connection.get_bucket(bucket_name)
        return bucket.get_key(key_name).content_type

    @staticmethod
    def stream_file(bucket_name, key_name):
        connection = boto.connect_s3()
        bucket = connection.get_bucket(bucket_name)

        for f in bucket.get_key(key_name):
            yield f

# /usr/bin/env python
# -*- coding: utf-8 -*-
import boto
import arrow
import uuid
from boto.s3.key import Key


class S3(object):

    @staticmethod
    def upload_string(bucket_name, key_name, contents, partition=True):
        """

        :param bucket_name:
        :param key_name:
        :param contents:
        :return:
        """
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
    def generate_form(bucket_name, expires_in=None, key_name=None, acl='private'):
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

        connection = boto.connect_s3()
        response = connection.build_post_form_args(bucket_name, key_name, expires_in=expires_in, acl=acl,
                                                   fields=fields, http_method='https', conditions=conditions)

        return response

    @staticmethod
    def generate_signed_url(bucket_name, method, expires_in=None, key_name=None):
        """
        Generates a signed URL to Amazon S3.

        :type bucket_name: str
        :param bucket_name: The name of the bucket to generate the upload url for
        :type expires_in: int|None
        :param expires_in: An integer in seconds until the generated URL expires. If not set it defaults to 1hr.
        :type key_name: str
        :param key_name:
        :type method: str
        :param method: Must be either GET or PUT. Will raise an exception
        :return: Returns a dictionary with the keys of signed_url, key_name, bucket
        :rtype: dict
        :raises: Exception
        """
        connection = boto.connect_s3()
        if not expires_in:
            expires_in = 3600

        if not key_name:
            date = arrow.utcnow().date()
            key_name = '%s/%s/%s/%s' % (date.day, date.month, date.year, uuid.uuid4())

        if method not in ['PUT', 'GET']:
            pass

        connection.generate_url_sigv4()

        signed_url = connection.generate_url(expires_in, method, bucket=bucket_name, key=key_name,
                                             headers={'Content-Type': 'applcation/octet-stream'})

        return {
            'bucket': bucket_name,
            'signed_url': signed_url,
            'key_name': key_name
        }

    @staticmethod
    def stream_file(bucket_name, key_name):
        connection = boto.connect_s3()
        bucket = connection.get_bucket(bucket_name)

        for f in bucket.get_key(key_name):
            yield f

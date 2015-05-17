# /usr/bin/env python
# -*- coding: utf-8 -*-
import boto
import arrow
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

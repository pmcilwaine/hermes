#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import boto.s3
import boto.rds2
from boto.exception import S3ResponseError
from hermes_aws import StackManager
import argparse


def format_name(args, name):
    return '%s-%s-%s' % (args.name, name, args.domain.replace('.', '-'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', required=True, help='Please enter a domain name')
    parser.add_argument('-n', '--name', required=True, help='Please enter the name of the cloud')
    parser.add_argument('-r', '--region', required=True, help='AWS Region to use')
    args = parser.parse_args()

    # delete buckets
    s3_conn = boto.s3.connect_to_region(args.region)
    for name in ['config', 'files', 'storage']:
        bucket_name = format_name(args, name)
        try:
            bucket = s3_conn.get_bucket(bucket_name)
            bucket.delete_keys(bucket.list())
            s3_conn.delete_bucket(bucket_name)
            print 'deleting bucket', bucket_name
        except S3ResponseError as e:
            print e.error_code, bucket_name

    # delete stacks
    stack_mgr = StackManager(args.region)
    print 'Deleting stacks'
    stack_mgr.delete_stacks(['{0}-{1}'.format(args.name, stack) for stack in ['jumpbox', 'cms', 'vpc']])

    return 0

if __name__ == '__main__':
    sys.exit(main())

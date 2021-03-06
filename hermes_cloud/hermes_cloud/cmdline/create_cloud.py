#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import uuid
import yaml
import boto
import urlparse
import boto.exception
import psycopg2
import boto.ec2
import boto.rds
from boto.rds2.exceptions import DBInstanceNotFound
import boto.s3
import argparse
from pkg_resources import resource_filename
from hermes_aws import StackManager, S3


class HermesCreateCloud(object):

    """
    It creates create_cloud callable program in your $PATH

    create_cloud -d [domain] -n [name] -m [manifest] -k [key] --region [region] --min [min] --max [max]

    Domain: The domain you wish to namespace your stacks too. This is recommended as S3 Buckets must be unique within
        all of AWS.

    Name: The name of the cloud. All stacks created are prefixed with this name

    Manifest: The AMI Manifest file to read to create the cloud

    Key: The AWS Key Pair used to assign to each instance for SSH login

    Region: The region to install the stacks. By default this is ap-southeast-2 (Sydney)

    Min: The minimum number of instances to have in the ASG.

    Max: The maximum number of instances to have in the ASG.
    """

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--domain', required=True, help='Please enter a domain name')
        parser.add_argument('-n', '--name', required=True, help='Please enter the name of the cloud')
        parser.add_argument('-m', '--manifest', required=True, help='The manifest of Images')
        parser.add_argument('-k', '--key', required=True, help='The key to assign to this cloud for SSH access')
        parser.add_argument('-r', '--region', required=True, help='AWS Region to use')
        parser.add_argument('--min', required=False, default=1, type=int,
                            help='The minimum number of instances in the auto-scaling group')
        parser.add_argument('--max', required=False, default=5, type=int,
                            help='The maximum number of instances in the auto-scaling group')
        parser.add_argument('-s', '--stack', required=True, help='The bucket to store the stack information for AWS.')
        self.args = parser.parse_args()

        self.tmpl_args = {
            'ssh_key': self.args.key,
            'name': self.args.name,
            'domain': self.args.domain,
            'config_bucket': self._format_name('config'),
            'files_bucket': self._format_name('files'),
            'storage_bucket': self._format_name('storage')
        }
        self.rds_config = {}
        self.params = {}
        self.stack_mgr = StackManager(self.args.region,
                                      name=self.args.name,
                                      params=self.params,
                                      tmpl_args=self.tmpl_args,
                                      template_path=[
                                          resource_filename('hermes_cloud', 'data/templates'),
                                          resource_filename('hermes_cloud', 'data/templates/includes')
                                      ],
                                      stack=self.args.stack)
        self.conn = boto.ec2.connect_to_region('ap-southeast-2')

        zone_names = ['AZ1', 'AZ2']
        zone_letters = ['a', 'b']

        availability_zones = dict(zip(zone_names,
                                      ['%s%s' % (self.args.region, letter)
                                       for letter in zone_letters]))

        self.tmpl_args.update({
            'availability_zones': availability_zones,
            'zone_names': zone_names
        })

    def _find_amis(self):
        amis = {}
        for ami in yaml.load(open(self.args.manifest))[0]['ami']:
            (name, image_name) = (ami.keys()[0], ami.values()[0])
            if image_name:
                image = self.conn.get_all_images(filters={'name': [image_name]})[0].id
                amis.update({name: image})

        return amis

    def _format_name(self, bucket):
        return '%s-%s-%s' % (self.args.name, bucket, self.args.domain.replace('.', '-'))

    def _create_buckets(self, buckets):
        conn = boto.s3.connect_to_region(self.args.region)
        for bucket in buckets:
            bucket_name = self._format_name(bucket)
            print 'Creating bucket %s' % (bucket_name, )
            try:
                conn.create_bucket(bucket_name, location=self.args.region)
            except boto.exception.S3CreateError:
                print 'Bucket %s already exists not creating' % (bucket_name, )

    def _generate_http_upload_policy(self, buckets):
        conn = boto.s3.connect_to_region(self.args.region)
        for bucket in buckets:
            _bucket = conn.get_bucket(self._format_name(bucket))
            _bucket.set_cors_xml('<?xml version="1.0" encoding="UTF-8"?><CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><CORSRule><AllowedOrigin>*</AllowedOrigin><AllowedMethod>GET</AllowedMethod><AllowedMethod>PUT</AllowedMethod><AllowedMethod>POST</AllowedMethod><MaxAgeSeconds>3000</MaxAgeSeconds><AllowedHeader>*</AllowedHeader></CORSRule></CORSConfiguration>')

    def _build_rds(self):
        try:
            config = json.loads(S3.get_string(self._format_name('config'), 'database'))
            parse = urlparse.urlparse(config['database'])
            (username, contents, port) = parse.netloc.split(':')
            (password, contents) = contents.split('@')

            self.tmpl_args['rds'] = {
                'username': username,
                'password': password,
                'db_name': self._format_name('cmsdb').replace('-', '_'),
                'instance_id': self._format_name('cmsdb')
            }
        except boto.exception.S3ResponseError:
            self.tmpl_args['rds'] = {
                'username': self._format_name('system_database').replace('-', '_'),
                'password': uuid.uuid4(),
                'db_name': self._format_name('cmsdb').replace('-', '_'),
                'instance_id': self._format_name('cmsdb')
            }

    def _upload_config_registry(self):
        for filename in ['blueprint', 'document', 'jobs', 'admin_rules']:
            data = json.loads(open(resource_filename('hermes_cloud',
                                                     'data/config_registry/{0}'.format(filename))).read())
            S3.upload_string(self._format_name('config'), filename, json.dumps(data), partition=False)

    def _create_config_database(self):
        conn = boto.rds2.connect_to_region(self.args.region)

        while True:
            try:
                describe = conn.describe_db_instances(self.tmpl_args['rds']['instance_id'])
                info = describe['DescribeDBInstancesResponse']['DescribeDBInstancesResult']['DBInstances'][0]
                if info['DBInstanceStatus'] == 'available':
                    # check if we have it in config already
                    try:
                        self.rds_config = json.loads(S3.get_string(self._format_name('config'), 'database'))
                    except boto.exception.S3ResponseError:
                        self.rds_config['database'] = 'postgres://{0}:{1}@{2}:{3}/{4}'.format(
                            self.tmpl_args['rds']['username'], self.tmpl_args['rds']['password'],
                            info['Endpoint']['Address'], '5432', self.tmpl_args['rds']['db_name']
                        )
                    break

                print 'rds', info['DBInstanceStatus']
            except DBInstanceNotFound as e:
                print 'Cannot find instance', str(e)

            time.sleep(10)

        S3.upload_string(self._format_name('config'), 'database', json.dumps(self.rds_config), partition=False)

    def _create_bucket_configs(self):
        for bucket in ['files', 'storage']:
            S3.upload_string(self._format_name('config'), bucket,
                             json.dumps({"bucket_name": self._format_name(bucket)}), partition=False)

    def _load_database(self):
        conn = boto.rds2.connect_to_region(self.args.region)
        describe = conn.describe_db_instances(self.tmpl_args['rds']['instance_id'])
        info = describe['DescribeDBInstancesResponse']['DescribeDBInstancesResult']['DBInstances'][0]

        # modify
        security_group_id = info['VpcSecurityGroups'][0]['VpcSecurityGroupId']
        security_group = self.conn.get_all_security_groups(group_ids=[security_group_id])[0]

        security_group.authorize(ip_protocol='tcp', from_port='5432', to_port='5432', cidr_ip='0.0.0.0/0')

        print 'connecting to db'
        db_conn = psycopg2.connect(self.rds_config['database'])

        cursor = db_conn.cursor()

        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'document')")
        record = cursor.fetchone()

        if record[0] is False:
            tables = open(resource_filename('hermes_cloud', 'data/database/create.sql'), 'r').read().split(';')
            for table in tables:
                try:
                    if table:
                        cursor.execute('{0};'.format(table))
                except psycopg2.ProgrammingError:
                    pass

            db_conn.commit()
            cursor.close()
            conn.close()

        security_group.revoke(ip_protocol='tcp', from_port='5432', to_port='5432', cidr_ip='0.0.0.0/0')

    def _create_queues_config(self):
        queues = {"queue": {}}
        for queue, queue_arn_label in (('multipage', 'MultipageSQS'), ('migrationdownload', 'MigrationDownloadSQS'),
                                       ('migrationupload', 'MigrationUploadSQS')):
            queues['queue'].update({queue: self.stack_mgr.stack_data['cms'][queue_arn_label]})

        S3.upload_string(self._format_name('config'), 'queues', json.dumps(queues), partition=False)

    def _create_cms_config(self):
        S3.upload_string(self._format_name('config'), 'cms', json.dumps({
            'dns': self.stack_mgr.stack_data['cms']['CMSFQDN'],
            'name': self.stack_mgr.stack_data['cms']['CMSLoadBalancerName']
        }), partition=False)

    def _create_topics_config(self):
        topics = {"topic": {}}
        for topic, topic_arn_label in (('multipage', 'MultipageSNS'), ('migrationdownload', 'MigrationDownloadSNS'),
                                       ('migrationupload', 'MigrationUploadSNS')):
            topics['topic'].update({topic: self.stack_mgr.stack_data['cms'][topic_arn_label]})

        S3.upload_string(self._format_name('config'), 'topics', json.dumps(topics), partition=False)

    def _create_region_config(self):
        S3.upload_string(self._format_name('config'), 'region', json.dumps({'region': self.args.region}),
                         partition=False)

    def deploy(self):
        for name, ami in self._find_amis().iteritems():
            self.params.update({name: [
                ('AMI', ami)
            ]})

            if name == "cms":
                self.params[name].extend([
                    ('MinInstances', self.args.min),
                    ('MinInstancesInService', 1),
                    ('MaxInstances', self.args.max)
                ])

        self.stack_mgr.add_stacks([
            'vpc',
            'jumpbox',
            'cms',
            'log'
        ])

        self._create_buckets([
            'files',
            'storage'
        ])
        self._build_rds()
        self.stack_mgr.create_stacks()
        print 'stacks created'
        self._upload_config_registry()
        print 'uploaded config registry'
        self._create_config_database()
        print 'created database config'
        self._create_bucket_configs()
        print 'created bucket configs'
        self._load_database()
        print 'loaded database'
        self._create_cms_config()
        print 'created cms config'
        self._create_region_config()
        print 'created region config'
        self._create_queues_config()
        print 'created queues config'
        self._create_topics_config()
        print 'created topics config'
        self._generate_http_upload_policy(['storage'])

def main():
    cloud = HermesCreateCloud()
    cloud.deploy()

if __name__ == '__main__':
    main()

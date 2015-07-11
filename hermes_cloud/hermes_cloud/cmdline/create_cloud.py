#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cloud Arguments
- name of cloud
- version of cloud
- domain

Optional Args
- CMS Min Instances
- CMS Max Instances
- Stacks bucket
"""

import argparse


class HermesCreateCloud(object):

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--domain', required=True, help='Please enter a domain name')
        parser.add_argument('-n', '--name', required=True, help='Please enter the name of the cloud')
        parser.add_argument('-v', '--version', required=True, help='The version of the cloud to base the AMIs from')
        parser.add_argument('--min', required=False, default=1, type=int,
                            help='The minimum number of instances in the auto-scaling group')
        parser.add_argument('--max', required=False, default=5, type=int,
                            help='The maximum number of instances in the auto-scaling group')
        parser.add_argument('-s', '--stack', required=False, help='The bucket to store the stack information for AWS.')
        self.args = parser.parse_args()

    def _create_bucket(self):
        pass

    def create(self):
        pass


def main():
    cloud = HermesCreateCloud()
    cloud.create()

if __name__ == '__main__':
    main()

# /usr/bin/env python
# -*- coding: utf-8 -*-
import boto.rds2


class RDS(object):

    def __init__(self, region):
        self.region = region
        self.conn = boto.rds2.connect_to_region(self.region)

    def _format_name(self, name):
        pass

    def create(self, name, username, password):
        pass

    def delete(self):
        pass

    def get_instance_info(self, name):
        pass

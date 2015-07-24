# /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import boto
import arrow
import boto.s3
import boto.cloudformation
from boto.exception import BotoServerError
from mako.lookup import TemplateLookup
from hermes_aws.s3 import S3


class StackManager(object):

    def __init__(self, region, name=None, params=None, tmpl_args=None, template_path=None, stack=None):
        """
        :type region: str
        :param region: The region to use to manage the stack
        :return:
        """
        if not isinstance(template_path, list) and template_path:
            template_path = [template_path]

        if params is None:
            params = {}

        self.conn = boto.cloudformation.connect_to_region(region)
        self.stack_name = name
        self.tmpl_args = tmpl_args
        self.params = params

        if template_path:
            self.template = TemplateLookup(directories=template_path)

        self.stacks = []
        self.stack_bucket = stack
        self.stack_path = '{0}/{1}'.format(self.params.get('version'), arrow.get().format('YYYY-MM-DD HH:mm:ss.SSSS'))
        self.stack_data = {}

    def add_stacks(self, stacks):
        if not isinstance(stacks, list):
            stacks = [stacks]

        self.stacks.extend(stacks)

    def _create_template(self, stack):
        self.tmpl_args.update({'stack_out': self.stack_data})
        return self.template.get_template("{0}.template".format(stack)).render(**self.tmpl_args)

    def validate_template(self, contents):
        """
        Validates the template before attempting to apply it.

        :type contents: str
        :param contents:
        :return: bool
        :raises BotoServerError
        """
        try:
            self.conn.validate_template(template_body=contents)
            return True
        except BotoServerError as e:
            print contents
            print e.message
            raise

    def _get_stack_information(self, stack_name, template=None):
        while True:
            stack = self.conn.describe_stacks(stack_name)[0]
            if stack.stack_status in ['CREATE_COMPLETE', 'UPDATE_COMPLETE']:

                for output in stack.outputs:
                    self.stack_data[template][output.key] = output.value

                return

            time.sleep(10)

    def create_stacks(self):
        """

        :return:
        """
        update_stack = True

        stack_names = {}
        for stack in self.stacks:
            stack_name = '{0}-{1}'.format(self.stack_name, stack)
            stack_names.update({stack: stack_name})
            try:
                self.conn.describe_stacks(stack_name)
            except BotoServerError:
                update_stack = False

        for stack in self.stacks:
            self.stack_data[stack] = {}
            print 'create template {0}'.format(stack)
            response = self._create_template(stack)
            print 'Validating template {0}'.format(stack)
            self.validate_template(response)
            print '{0} template valid'.format(stack)

            # upload to stacks
            full_path = '{0}/{1}.template'.format(self.stack_path, stack)
            S3.upload_string(self.stack_bucket, full_path, response)

            try:
                if update_stack:
                    pass
                else:
                    self.conn.create_stack(stack_names[stack], template_body=response,
                                           parameters=self.params.get(stack),
                                           capabilities=['CAPABILITY_IAM'])
            except Exception as e:
                print 'Template Failed'
                print response
                raise e

            self._get_stack_information(stack_names[stack], stack)

    def delete_stacks(self, stacks):
        """
        Will delete a list of stacks

        :type stacks: list
        :param stacks:
        :return:
        """

        for stack in stacks:
            self.conn.delete_stack(stack)

        print 'Attempting to delete stacks', ', '.join(stacks)
        while stacks:
            for stack in stacks:
                try:
                    info = self.conn.describe_stacks(stack)[0]
                    if info.stack_status == 'DELETE_FAILED':
                        self.conn.delete_stack(stack)
                except BotoServerError as e:
                    if e.error_code == 'ValidationError':
                        stacks.remove(stack)
                        print stack, 'deleted.'

            if stacks:
                time.sleep(10)

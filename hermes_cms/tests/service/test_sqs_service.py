# /usr/bin/env python
# -*- coding: utf-8 -*-
import boto
import pytest
from hermes_cms.service.sqs_service import SQSService, SQSNotExistError
from mock import patch, MagicMock
from moto import mock_sqs


@pytest.fixture
def basic_config():
    return {
        'jobs': {
            'job_name': {
                'module_name': 'hermes_cms',
                'class_name': 'SQSService',
                'service': {
                    'service_module': 'hermes_cms',
                    'service_class': 'TestJob',
                    'topic': '',
                    'queue': 'test-queue',
                    'messages': 1
                }
            }
        }
    }


@mock_sqs
@patch('hermes_cms.service.service.import_handler')
def test_initialise_service(mock_import_handler, basic_config):
    conn = boto.connect_sqs()
    conn.create_queue('test-queue')

    mock_import_handler.return_value = MagicMock()
    service = SQSService('job_name', 'ap-southeast-2', basic_config)
    assert service.queue.name == 'test-queue'


@mock_sqs
@patch('hermes_cms.service.service.import_handler')
def test_missing_queue(mock_import_handler, basic_config):
    conn = boto.connect_sqs()
    conn.create_queue('invalid-queue')

    mock_import_handler.return_value = MagicMock()
    with pytest.raises(SQSNotExistError):
        SQSService('job_name', 'ap-southeast-2', basic_config)

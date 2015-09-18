# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import boto
import pytest
import base64
from datetime import datetime
from mock import patch, MagicMock, call
from moto import mock_s3
from boto.s3.key import Key
from boto.sqs.message import Message
from hermes_cms.service.job import InvalidJobError, FatalJobError
from hermes_cms.service.multipage import MultipageJob

zip_fileb64 = 'UEsDBAoAAAAAABFk+UZxwozlFQAAABUAAAAKABwAaW5kZXguaHRtbFVUCQADQfWyVUH1slV1eAsAAQT1AQAABBQAAAA8aDE+SGVsbG8gV29ybGQ8L2gxPgpQSwECHgMKAAAAAAARZPlGccKM5RUAAAAVAAAACgAYAAAAAAABAAAApIEAAAAAaW5kZXguaHRtbFVUBQADQfWyVXV4CwABBPUBAAAEFAAAAFBLBQYAAAAAAQABAFAAAABZAAAAAAA='


def side_effect(value):
    return {
        'database': MagicMock(),
        'storage': {'bucket_name': 'storage-bucket'},
        'files': {'bucket_name': 'files-bucket'}
    }.get(value)


@patch('hermes_cms.service.multipage.connectionForURI')
@patch('hermes_cms.service.multipage.Registry')
def test_do_work_with_no_message(registry_mock, connection_mock):
    service = MultipageJob()
    service.do_work()


@mock_s3
@patch('hermes_cms.service.multipage.connectionForURI')
@patch('hermes_cms.service.multipage.Registry')
def test_do_work_message_invalid_job(registry_mock, connection_mock):
    conn_s3 = boto.connect_s3()
    conn_s3.create_bucket('storage-bucket')
    conn_s3.create_bucket('files-bucket')

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)

    registry_mock.return_value = registry

    message = Message()
    message.set_body(json.dumps({
        'Message': '9bd96ca7-3d0a-4e74-b523-b3bd38e9862e',
        'Subject': 'Test Subject'
    }))

    service = MultipageJob()
    with pytest.raises(InvalidJobError):
        service.do_work(message)


@mock_s3
@patch('hermes_cms.service.multipage.connectionForURI')
@patch('hermes_cms.service.multipage.Registry')
@patch('hermes_cms.service.multipage.Document')
@patch('hermes_cms.service.multipage.JobDB')
def test_do_work_invalid_document(jobdb_mock, document_mock, registry_mock, connection_mock):
    conn_s3 = boto.connect_s3()
    storage = conn_s3.create_bucket('storage-bucket')
    files = conn_s3.create_bucket('files-bucket')

    key = Key(storage, '25/7/2015/56d3c182-f72f-4216-9e94-1756bf67564d')
    key.set_contents_from_string(base64.decodestring(zip_fileb64))

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)

    registry_mock.return_value = registry

    message = Message()
    message.set_body(json.dumps({
        'Message': '9bd96ca7-3d0a-4e74-b523-b3bd38e9862e',
        'Subject': 'Test Subject'
    }))

    job = MagicMock(**{
        'uuid': '9bd96ca7-3d0a-4e74-b523-b3bd38e9862e',
        'name': 'Multipage Doc',
        'status': 'pending',
        'created': datetime(2015, 7, 25, 12, 0, 0),
        'modified': datetime(2015, 7, 25, 12, 0, 0),
        'message': {
            'document': '56d3c182-f72f-4216-9e94-1756bf67564d',
            'on_complete': {
                'alter': {}
            }
        }
    })
    job.set = MagicMock()

    jobdb_mock.selectBy.return_value.getOne.return_value = job
    document_mock.selectBy.return_value.getOne.return_value = None

    service = MultipageJob()
    with pytest.raises(FatalJobError):
        service.do_work(message)

    assert job.set.call_args_list == [call(status='running'),
                                      call(message={'document': '56d3c182-f72f-4216-9e94-1756bf67564d',
                                                    'on_complete': {'alter': {}}, 'reason': 'No Document exists'},
                                           status='failed')]


@mock_s3
@patch('hermes_cms.service.multipage.connectionForURI')
@patch('hermes_cms.service.multipage.Registry')
@patch('hermes_cms.service.multipage.Document')
@patch('hermes_cms.service.multipage.JobDB')
def test_do_work_valid_job(jobdb_mock, document_mock, registry_mock, connection_mock):
    conn_s3 = boto.connect_s3()
    storage = conn_s3.create_bucket('storage-bucket')
    files = conn_s3.create_bucket('files-bucket')

    key = Key(storage, '25/7/2015/56d3c182-f72f-4216-9e94-1756bf67564d')
    key.set_contents_from_string(base64.decodestring(zip_fileb64))

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)

    registry_mock.return_value = registry

    message = Message()
    message.set_body(json.dumps({
        'Message': '9bd96ca7-3d0a-4e74-b523-b3bd38e9862e',
        'Subject': 'Test Subject'
    }))

    job = MagicMock(**{
        'uuid': '9bd96ca7-3d0a-4e74-b523-b3bd38e9862e',
        'name': 'Multipage Doc',
        'status': 'pending',
        'created': datetime(2015, 7, 25, 12, 0, 0),
        'modified': datetime(2015, 7, 25, 12, 0, 0),
        'message': {
            'document': '56d3c182-f72f-4216-9e94-1756bf67564d',
            'on_complete': {
                'alter': {}
            }
        }
    })
    job.set = MagicMock()

    document = MagicMock(**{
        'uuid': '56d3c182-f72f-4216-9e94-1756bf67564d'
    })

    jobdb_mock.selectBy.return_value.getOne.return_value = job
    document_mock.selectBy.return_value.getOne.return_value = document
    document_mock.get_document.return_value = {
        'document': {},
        'file': {
            'key': '25/7/2015/56d3c182-f72f-4216-9e94-1756bf67564d'
        }
    }

    service = MultipageJob()
    service.do_work(message)

    assert Key(files, '56d3c182-f72f-4216-9e94-1756bf67564d/index.html').exists()
    assert job.set.call_args_list == [call(status='running'), call(status='complete')]

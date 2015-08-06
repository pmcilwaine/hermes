# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import boto
import pytest
import zipfile
from datetime import datetime
from cStringIO import StringIO
from boto.s3.key import Key
from moto import mock_s3
from sqlobject.sqlbuilder import IN
from boto.sqs.message import Message
from hermes_cms.service.job import InvalidJobError
from hermes_cms.service.migration_download import MigrationDownloadJob
from mock import patch, MagicMock, call


def side_effect(value):
    return {
        'database': MagicMock(),
        'storage': {'bucket_name': 'storage-bucket'},
        'files': {'bucket_name': 'files-bucket'},
    }.get(value)


@mock_s3
@patch('hermes_cms.service.migration_download.connectionForURI')
@patch('hermes_cms.service.migration_download.Registry')
def test_do_work_with_no_message(registry_mock, connection_mock):
    conn_s3 = boto.connect_s3()
    conn_s3.create_bucket('storage-bucket')
    conn_s3.create_bucket('files-bucket')

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)

    registry_mock.return_value = registry

    service = MigrationDownloadJob()
    service.do_work()


@mock_s3
@patch('hermes_cms.service.migration_download.connectionForURI')
@patch('hermes_cms.service.migration_download.Registry')
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

    service = MigrationDownloadJob()
    with pytest.raises(InvalidJobError):
        service.do_work(message)


@mock_s3
@patch('hermes_cms.service.migration_download.JobDB')
@patch('hermes_cms.service.migration_download.Document')
@patch('hermes_cms.service.migration_download.connectionForURI')
@patch('hermes_cms.service.migration_download.Registry')
def test_single_document_has_get_doc_call(registry_mock, connection_mock, document_mock, job_mock):
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

    job = MagicMock(**{
        'uuid': '9bd96ca7-3d0a-4e74-b523-b3bd38e9862e',
        'name': 'Migration Download',
        'status': 'pending',
        'message': {
            'documents': [
                {'parent_id': '56d3c182-f72f-4216-9e94-1756bf67564d'}
            ]
        }
    })
    job.set = MagicMock()

    job_mock.selectBy.return_value.getOne.return_value = job

    service = MigrationDownloadJob()
    with patch.object(service, '_get_document_query') as method_mock:
        service.do_work(message)
        assert method_mock.called

    assert job.set.call_args_list == [call(status='running'), call(status='complete')]


@mock_s3
@patch.object(MigrationDownloadJob, '_get_document_query')
@patch.object(MigrationDownloadJob, '_get_document_parent_url')
@patch('hermes_cms.service.migration_download.JobDB')
@patch('hermes_cms.service.migration_download.Document')
@patch('hermes_cms.service.migration_download.connectionForURI')
@patch('hermes_cms.service.migration_download.Registry')
def test_single_path_document_zip(registry_mock, connection_mock, document_mock, job_mock, parent_url_mock, get_document_mock):
    conn_s3 = boto.connect_s3()
    bucket = conn_s3.create_bucket('storage-bucket')
    conn_s3.create_bucket('files-bucket')

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
        'name': 'Migration Download',
        'status': 'pending',
        'message': {
            'documents': [
                {'parent_id': '56d3c182-f72f-4216-9e94-1756bf67564d'}
            ]
        }
    })
    job.set = MagicMock()

    document_mock.query.return_value = [MagicMock(**{
        'uuid': '56d3c182-f72f-4216-9e94-1756bf67564d',
        'created': datetime(2015, 5, 17)
    }), MagicMock(**{
        'uuid': '79254d0b-0902-4697-89d1-4be8ff3acd69',
        'created': datetime(2015, 5, 17)
    })]

    key1 = Key(bucket, '17/5/2015/56d3c182-f72f-4216-9e94-1756bf67564d')
    key1.set_contents_from_string(json.dumps({
        'document': {
            'id': 1,
            'uuid': '56d3c182-f72f-4216-9e94-1756bf67564d',
            'created': str(datetime(2015, 5, 17)),
            'url': '/',
            'parent': 0,
            'path': '1/'
        }
    }))

    key2 = Key(bucket, '17/5/2015/79254d0b-0902-4697-89d1-4be8ff3acd69')
    key2.set_contents_from_string(json.dumps({
        'document': {
            'id': 2,
            'uuid': '79254d0b-0902-4697-89d1-4be8ff3acd69',
            'created': str(datetime(2015, 5, 17)),
            'url': 'test',
            'parent': 1,
            'path': '1/2'
        },
        'file': {
            "bucket": "storage-bucket",
            'key': '17/5/2015/a984dea7-8140-44cb-80a0-7e832ff1ff19'
        }
    }))

    key3 = Key(bucket, '17/5/2015/a984dea7-8140-44cb-80a0-7e832ff1ff19')
    key3.set_contents_from_string('Hello World')

    job_mock.selectBy.return_value.getOne.return_value = job

    service = MigrationDownloadJob()

    get_document_mock.return_value = IN('uuid', [
        '56d3c182-f72f-4216-9e94-1756bf67564d',
        '79254d0b-0902-4697-89d1-4be8ff3acd69'
    ])

    def parent_side_effects(parent_id):
        return '/' if parent_id else ''

    parent_url_mock.side_effect = parent_side_effects

    service.do_work(message)

    key = Key(bucket, '9bd96ca7-3d0a-4e74-b523-b3bd38e9862e')
    contents = StringIO(key.get_contents_as_string())
    handle = zipfile.ZipFile(contents, 'r', compression=zipfile.ZIP_DEFLATED)
    assert key.exists()
    assert handle.namelist() == ['56d3c182-f72f-4216-9e94-1756bf67564d', '79254d0b-0902-4697-89d1-4be8ff3acd69',
                                 '17/5/2015/a984dea7-8140-44cb-80a0-7e832ff1ff19', 'manifest']
    assert job.set.call_args_list == [call(status='running'), call(status='complete')]

# /usr/bin/env python
# -*- coding: utf-8 -*-
import boto
import json
import pytest
import zipfile
from moto import mock_s3
from boto.s3.key import Key
from cStringIO import StringIO
from mock import patch, MagicMock, call
from boto.sqs.message import Message
from hermes_cms.service.job import InvalidJobError
from hermes_cms.service.migration_upload import MigrationUploadJob


def side_effect(value):
    return {
        'database': MagicMock(),
        'storage': {'bucket_name': 'storage-bucket'},
        'files': {'bucket_name': 'file-bucket'}
    }.get(value)


@mock_s3
@patch('hermes_cms.service.migration_upload.connectionForURI')
@patch('hermes_cms.service.migration_upload.Registry')
def test_do_work_with_no_message(registry_mock, connection_mock):
    conn_s3 = boto.connect_s3()
    conn_s3.create_bucket('storage-bucket')
    conn_s3.create_bucket('file-bucket')

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)

    registry_mock.return_value = registry

    service = MigrationUploadJob()
    service.do_work()


@mock_s3
@patch('hermes_cms.service.migration_upload.connectionForURI')
@patch('hermes_cms.service.migration_upload.Registry')
def test_do_work_message_invalid_job(registry_mock, connection_mock):
    conn_s3 = boto.connect_s3()
    conn_s3.create_bucket('storage-bucket')
    conn_s3.create_bucket('file-bucket')

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)

    registry_mock.return_value = registry

    message = Message()
    message.set_body(json.dumps({
        'Message': '9bd96ca7-3d0a-4e74-b523-b3bd38e9862e',
        'Subject': 'Test Subject'
    }))

    service = MigrationUploadJob()
    with pytest.raises(InvalidJobError):
        service.do_work(message)


@mock_s3
@patch('hermes_cms.service.migration_upload.connectionForURI')
@patch('hermes_cms.service.migration_upload.Registry')
@patch('hermes_cms.service.migration_upload.JobDB')
def test_archive_cannot_be_found(job_mock, registry_mock, connection_mock):
    conn_s3 = boto.connect_s3()
    storage = conn_s3.create_bucket('storage-bucket')
    conn_s3.create_bucket('file-bucket')

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
            'file': {
                'key': 'archive.zip'
            }
        }
    })

    job_mock.selectBy.return_value.getOne.return_value = job

    service = MigrationUploadJob()
    with pytest.raises(InvalidJobError):
        service.do_work(message)

    assert job.set.called


@mock_s3
@patch('hermes_cms.service.migration_upload.connectionForURI')
@patch('hermes_cms.service.migration_upload.Registry')
@patch('hermes_cms.service.migration_upload.JobDB')
def test_invalid_archive_missing_manifest(job_mock, registry_mock, connection_mock):
    conn_s3 = boto.connect_s3()
    storage = conn_s3.create_bucket('storage-bucket')
    conn_s3.create_bucket('file-bucket')

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
            'file': {
                'key': 'archive.zip'
            }
        }
    })

    job_mock.selectBy.return_value.getOne.return_value = job

    key = Key(storage, 'archive.zip')
    fp = StringIO()
    handle = zipfile.ZipFile(fp, mode='w', compression=zipfile.ZIP_DEFLATED)
    handle.writestr('test', json.dumps({'content': 'Hello World'}))
    handle.close()
    key.set_contents_from_string(fp.getvalue())

    service = MigrationUploadJob()
    with pytest.raises(InvalidJobError):
        service.do_work(message)

    assert job.set.call_args_list == [call(status='running'),
                                      call(message={'file': {'key': 'archive.zip'},
                                                     'reason': 'Unable to retrieve manifest in archive'},
                                           status='failed')]


@mock_s3
@patch.object(MigrationUploadJob, '_validate_manifest')
@patch.object(MigrationUploadJob, '_get_manifest')
@patch('hermes_cms.service.migration_upload.connectionForURI')
@patch('hermes_cms.service.migration_upload.Registry')
@patch('hermes_cms.service.migration_upload.JobDB')
def test_validate_manifest_fail(job_mock, registry_mock, connection_mock, manifest_mock, method_mock):
    conn_s3 = boto.connect_s3()
    storage = conn_s3.create_bucket('storage-bucket')
    conn_s3.create_bucket('file-bucket')

    manifest_mock.return_value = {'documents': None}
    method_mock.return_value = False

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
            'file': {
                'key': 'archive.zip'
            },
            'user_id': 1  # used to replace old document user
        }
    })

    key = Key(storage, 'archive.zip')
    fp = StringIO()
    handle = zipfile.ZipFile(fp, mode='w', compression=zipfile.ZIP_DEFLATED)
    handle.close()
    key.set_contents_from_string(fp.getvalue())

    job_mock.selectBy.return_value.getOne.return_value = job

    service = MigrationUploadJob()
    with pytest.raises(InvalidJobError):
        service.do_work(message)

    assert job.set.call_args_list == [call(status='running'),
                                      call(message={'reason': 'Manifest found is not valid', 'user_id': 1,
                                                    'file': {'key': 'archive.zip'}},
                                           status='failed')]


@mock_s3
@patch.object(MigrationUploadJob, '_validate_manifest')
@patch('hermes_cms.service.migration_upload.connectionForURI')
@patch('hermes_cms.service.migration_upload.Registry')
@patch('hermes_cms.service.migration_upload.JobDB')
@patch('hermes_cms.service.migration_upload.Document')
def test_single_document_upload_validate(document_mock, job_mock, registry_mock, connection_mock, method_mock):
    conn_s3 = boto.connect_s3()
    storage = conn_s3.create_bucket('storage-bucket')
    conn_s3.create_bucket('file-bucket')

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)

    registry_mock.return_value = registry
    method_mock.return_value = True

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
            'file': {
                'key': 'archive.zip'
            },
            'user_id': 1  # used to replace old document user
        }
    })

    job_mock.selectBy.return_value.getOne.return_value = job

    key = Key(storage, 'archive.zip')
    fp = StringIO()
    handle = zipfile.ZipFile(fp, mode='w', compression=zipfile.ZIP_DEFLATED)
    handle.writestr('manifest', json.dumps({'documents': [{
        'uuid': '98f0d33d-2c71-4169-a44f-a4050c4854fb', 'url': 'a-new-page',
        'parent_url': 'test', 'parent_uuid': 'f0bf7b1a-4fe8-4a7a-b8ab-4b56e9ea8a36'}],
        'full': False
    }))
    handle.writestr('98f0d33d-2c71-4169-a44f-a4050c4854fb', json.dumps({
        'document': {
            "archived": False,
            "name": "A new Page",
            "parent": 10,
            "created": "2015-06-01T12:52:26.865154+00:00",
            "url": "a-new-page",
            "menutitle": "Home",
            "show_in_menu": False,
            "user": 1,
            "published": True,
            "path": "10/3/",
            "type": "Page",
            "uuid": "98f0d33d-2c71-4169-a44f-a4050c4854fb"
        }, "page": {
            "content": "<p>Homepage</p>\n<p>Modified</p>",
            "template": "Standard"
        }
    }))
    handle.close()
    key.set_contents_from_string(fp.getvalue())

    document_mock.selectBy.return_value.getOne.return_value = MagicMock(**{
        'uuid': 'f0bf7b1a-4fe8-4a7a-b8ab-4b56e9ea8a36',
        'path': '1/',
        'url': 'test',
        'id': 1,
        'parent': 0
    })

    service = MigrationUploadJob()
    service.do_work(message)

    assert Key(storage, '1/6/2015/98f0d33d-2c71-4169-a44f-a4050c4854fb').exists()
    assert job.set.call_args_list == [call(status='running'), call(status='complete')]


@mock_s3
@patch.object(MigrationUploadJob, '_validate_manifest')
@patch('hermes_cms.service.migration_upload.connectionForURI')
@patch('hermes_cms.service.migration_upload.Registry')
@patch('hermes_cms.service.migration_upload.JobDB')
@patch('hermes_cms.service.migration_upload.Document')
def test_document_with_file(document_mock, job_mock, registry_mock, connection_mock, method_mock):
    conn_s3 = boto.connect_s3()
    storage = conn_s3.create_bucket('storage-bucket')
    file_bucket = conn_s3.create_bucket('file-bucket')

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)

    registry_mock.return_value = registry
    method_mock.return_value = True

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
            'file': {
                'key': 'archive.zip'
            },
            'user_id': 1  # used to replace old document user
        }
    })
    job.set = MagicMock()

    job_mock.selectBy.return_value.getOne.return_value = job

    key = Key(storage, 'archive.zip')
    fp = StringIO()
    handle = zipfile.ZipFile(fp, mode='w', compression=zipfile.ZIP_DEFLATED)
    handle.writestr('manifest', json.dumps({'documents': [{
        'uuid': '98f0d33d-2c71-4169-a44f-a4050c4854fb', 'url': 'a-new-page',
        'parent_url': 'test', 'parent_uuid': 'f0bf7b1a-4fe8-4a7a-b8ab-4b56e9ea8a36'}],
        'full': False
    }))
    handle.writestr('98f0d33d-2c71-4169-a44f-a4050c4854fb', json.dumps({
        'document': {
            "archived": False,
            "name": "A new Page",
            "parent": 10,
            "created": "2015-06-01T12:52:26.865154+00:00",
            "url": "a-new-page",
            "menutitle": "Home",
            "show_in_menu": False,
            "user": 1,
            "published": True,
            "path": "10/3/",
            "type": "File",
            "uuid": "98f0d33d-2c71-4169-a44f-a4050c4854fb"
        }, "file": {
            "type": "text/plain",
            "bucket": "storage",
            "name": "hello.txt",
            "key": "3/6/2015/c1ad1745-d3b8-40b7-a945-4f365e84f054"
        }
    }))
    handle.writestr('file/3/6/2015/c1ad1745-d3b8-40b7-a945-4f365e84f054', 'stuff')
    handle.close()
    key.set_contents_from_string(fp.getvalue())

    document_mock.selectBy.return_value.getOne.return_value = MagicMock(**{
        'uuid': 'f0bf7b1a-4fe8-4a7a-b8ab-4b56e9ea8a36',
        'path': '1/',
        'url': 'test',
        'id': 1,
        'parent': 0
    })

    service = MigrationUploadJob()
    service.do_work(message)

    assert Key(storage, '1/6/2015/98f0d33d-2c71-4169-a44f-a4050c4854fb').exists()
    assert Key(storage, '3/6/2015/c1ad1745-d3b8-40b7-a945-4f365e84f054').exists()
    assert job.set.call_args_list == [call(status='running'), call(status='complete')]

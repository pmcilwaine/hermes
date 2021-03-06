# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import arrow
import pytest
import boto.sns
from moto import mock_sns
from mock import MagicMock, patch
from hermes_cms.core.auth import Auth
from hermes_cms.app import create_app


def app():
    """
    :return: flask.Flask
    """
    return create_app().test_client()


@pytest.fixture()
def admin_rules_config():
    instance = MagicMock(name='Registry')
    instance.get.return_value = {
        'rules': [
            {
                "name": "migration_upload",
                "url": "/migration_upload",
                "module_name": "hermes_cms.controller.admin.migration_upload",
                "class_name": "MigrationUpload",
                "methods": ["POST"]
            }
        ]
    }

    return instance


@pytest.fixture()
def blueprint_config():
    instance = MagicMock(name='Registry')
    instance.get.return_value = {
        'blueprint': [
            {
                'name': 'hermes_cms.views.admin',
                'from': 'route'
            }
        ]
    }

    return instance


@patch.object(Auth, 'has_permission')
@patch('hermes_cms.views.admin.Registry')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_invalid_post(config_mock, db_connect_mock, registry_mock, permission_mock, blueprint_config, admin_rules_config):
    config_mock.return_value = blueprint_config
    registry_mock.return_value = admin_rules_config
    db_connect_mock.return_value = None
    permission_mock.return_value = True
    response = app().post('/admin/migration_upload')
    assert response.status_code == 400


@patch.object(Auth, 'has_permission')
@patch('hermes_cms.views.admin.Registry')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_post_invalid_data(config_mock, db_connect_mock, _mock, permission_mock, blueprint_config):
    config_mock.return_value = blueprint_config
    db_connect_mock.return_value = None
    permission_mock.return_value = True
    response = app().post('/admin/migration_upload', data=json.dumps({
        'test': {}
    }), content_type='application/json')
    assert response.status_code == 400


@mock_sns
@patch.object(Auth, 'has_permission')
@patch('hermes_cms.views.admin.Registry')
@patch('hermes_cms.controller.admin.migration_upload.session')
@patch('hermes_cms.controller.admin.migration_upload.arrow')
@patch('hermes_cms.controller.admin.migration_upload.Registry')
@patch('hermes_cms.controller.admin.migration_upload.Job')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_post_specific_documents(app_registry, db_connect_mock, job_mock, registry_mock, arrow_mock, session_mock,
                                 _mock, permission_mock, blueprint_config):
    arrow_mock.now.return_value = arrow.get(2015, 7, 1, 20, 0, 0)

    conn = boto.sns.connect_to_region('ap-southeast-2')
    topic = conn.create_topic('migration_upload')

    session_mock.return_value = {}
    app_registry.return_value = blueprint_config

    permission_mock.return_value = True

    def side_effect(value):
        return {
            'topics': {'topic': {'migrationupload': topic['CreateTopicResponse']['CreateTopicResult']['TopicArn']}},
            'region': {'region': 'ap-southeast-2'}
        }.get(value)

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)
    registry_mock.return_value = registry

    db_connect_mock.return_value = None

    response = app().post('/admin/migration_upload', data=json.dumps({
        'file': {
            'name': 'test.zip',
            'bucket': 'test'
        }
    }), content_type='application/json')

    job_mock.save.return_value = MagicMock(**{
        'uuid': 'job-id'
    })

    assert response.status_code == 200
    assert job_mock.save.called

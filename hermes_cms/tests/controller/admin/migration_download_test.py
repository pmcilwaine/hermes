# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import arrow
import pytest
import boto.sns
from moto import mock_sns
from mock import MagicMock, patch
from hermes_cms.app import create_app


def app():
    """

    :return: flask.Flask
    """
    return create_app().test_client()


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


@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_invalid_post(config_mock, db_connect_mock, blueprint_config):
    config_mock.return_value = blueprint_config
    db_connect_mock.return_value = None
    response = app().post('/admin/migration')
    assert response.status_code == 400


@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_post_invalid_data(config_mock, db_connect_mock, blueprint_config):
    config_mock.return_value = blueprint_config
    db_connect_mock.return_value = None
    response = app().post('/admin/migration', data=json.dumps({
        'document': [{'parent_id': 'uuid'}],
        'all_documents': True
    }), content_type='application/json')
    assert response.status_code == 400


@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_post_invalid_data_2(config_mock, db_connect_mock, blueprint_config):
    config_mock.return_value = blueprint_config
    db_connect_mock.return_value = None
    response = app().post('/admin/migration', data=json.dumps({
        'document': [],
        'all_documents': False
    }), content_type='application/json')
    assert response.status_code == 400


@mock_sns
@patch('hermes_cms.controller.admin.migration_download.arrow')
@patch('hermes_cms.controller.admin.migration_download.Registry')
@patch('hermes_cms.controller.admin.migration_download.Job')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_post_specific_documents(app_registry, db_connect_mock, job_mock, registry_mock, arrow_mock, blueprint_config):

    arrow_mock.now.return_value = arrow.get(2015, 7, 1, 20, 0, 0)

    conn = boto.sns.connect_to_region('ap-southeast-2')
    topic = conn.create_topic('migration_download')

    app_registry.return_value = blueprint_config

    def side_effect(value):
        return {
            'topics': {'topic': {'migrationdownload': topic['CreateTopicResponse']['CreateTopicResult']['TopicArn']}},
            'region': {'region': 'ap-southeast-2'}
        }.get(value)

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)
    registry_mock.return_value = registry

    db_connect_mock.return_value = None

    response = app().post('/admin/migration', data=json.dumps({
        "document": [],
        "all_documents": True
    }), content_type='application/json')

    job_mock.save.return_value = MagicMock(**{
        'uuid': 'job-id'
    })

    assert response.status_code == 200
    assert job_mock.save.called


@mock_sns
@patch('hermes_cms.controller.admin.migration_download.arrow')
@patch('hermes_cms.controller.admin.migration_download.Registry')
@patch('hermes_cms.controller.admin.migration_download.Job')
@patch('hermes_cms.app.db_connect')
@patch('hermes_cms.app.Registry')
def test_post_specific_documents_2(app_registry, db_connect_mock, job_mock, registry_mock, arrow_mock, blueprint_config):

    arrow_mock.now.return_value = arrow.get(2015, 7, 1, 20, 0, 0)

    conn = boto.sns.connect_to_region('ap-southeast-2')
    topic = conn.create_topic('migration_download')

    app_registry.return_value = blueprint_config

    def side_effect(value):
        return {
            'topics': {'topic': {'migrationdownload': topic['CreateTopicResponse']['CreateTopicResult']['TopicArn']}},
            'region': {'region': 'ap-southeast-2'}
        }.get(value)

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)
    registry_mock.return_value = registry

    db_connect_mock.return_value = None

    response = app().post('/admin/migration', data=json.dumps({
        "document": [{"parent_id": "some-uuid"}],
        "all_documents": False
    }), content_type='application/json')

    job_mock.save.return_value = MagicMock(**{
        'uuid': 'job-id'
    })

    assert response.status_code == 200
    assert job_mock.save.called

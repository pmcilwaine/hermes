# /usr/bin/env python
# -*- coding: utf-8 -*-

import boto.sns
from mock import MagicMock, patch, call
from moto import mock_sns
from hermes_cms.helpers.multipage import Multipage


@mock_sns
@patch('hermes_cms.helpers.multipage.Registry')
@patch('hermes_cms.helpers.multipage.Job')
def test_do_work(job_mock, registry_mock):

    conn = boto.sns.connect_to_region('ap-southeast-2')
    topic = conn.create_topic('multipage-test')

    def side_effect(value):
        return {
            'topics': {'topic': {'multipage': topic['CreateTopicResponse']['CreateTopicResult']['TopicArn']}},
            'region': {'region': 'ap-southeast-2'}
        }.get(value)

    registry = MagicMock()
    registry.get = MagicMock(side_effect=side_effect)
    registry_mock.return_value = registry

    document = MagicMock(**{
        'uuid': 'some-id',
        'published': True
    })
    document.name = 'Test Document'

    job_mock.save.return_value = MagicMock(**{
        'uuid': 'job-id'
    })

    helper = Multipage(document)
    helper.do_work()

    assert document.set.called
    assert job_mock.save.called

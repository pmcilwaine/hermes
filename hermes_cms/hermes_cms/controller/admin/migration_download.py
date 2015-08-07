# /usr/bin/env python
# -*- coding: utf-8 -*-
import arrow
import boto.sns
from boto.exception import BotoServerError
import logging
from flask import request, Response
from flask.views import MethodView
from hermes_cms.db import Job
from hermes_cms.core.registry import Registry

log = logging.getLogger('hermes_cms.controller.admin.multipage_download')


class MigrationDownload(MethodView):

    # pylint: disable=no-self-use
    def get(self):
        """

        :rtype: flask.Response
        :return: A flask Response object
        """
        return ''

    # pylint: disable=no-self-use
    def post(self):
        """

        For specific parents

        {
            "documents": [{
                "parent_id": "uuid"
            }],
            "all_documents": false
        }

        {
            "documents": [],
            "all_documents": true
        }

        :rtype: flask.Response
        :return: A flask Response object
        """
        data = request.json

        if not data:
            return Response(status=400)

        if not ((data.get('document') and not data.get('all_documents')) or
                (not data.get('document') and data.get('all_documents'))):
            return Response(status=400)

        name = 'Migration Download {0}'.format(arrow.now().format('YYYY-MM-DD HH:mm'))
        job = Job.save({
            'name': name,
            'status': 'pending',
            'message': data
        })

        topic_arn = Registry().get('topics').get('topic').get('migrationdownload')
        conn = boto.sns.connect_to_region(Registry().get('region').get('region'))

        try:
            conn.publish(topic_arn, str(job.uuid), name)
        except BotoServerError as e:
            log.error('Cannot publish Job=%s to Topic=%s', job.uuid, topic_arn)
            log.exception(e)
            return Response(status=500)
        except AttributeError as e:
            log.error('Cannot publish Job=%s to Topic=%s "%s"', job.uuid, topic_arn, str(e))
            return Response(status=500)

        return Response(status=200)

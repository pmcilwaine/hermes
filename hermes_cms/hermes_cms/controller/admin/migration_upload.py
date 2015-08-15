# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import arrow
import logging
import boto.sns
from hermes_cms.db import Job
from flask.views import MethodView
from flask import request, Response, session
from boto.exception import BotoServerError
from hermes_cms.core.registry import Registry

log = logging.getLogger('hermes_cms.controller.admin.multipage_upload')


class MigrationUpload(MethodView):

    # pylint: disable=no-self-use
    def post(self):
        data = request.json
        if not data or not data.get('file'):
            return Response(status=400)

        data['user_id'] = session['auth_user'].get('id', -1)

        name = data.get('name', 'Migration Upload {0}'.format(arrow.now().format('YYYY-MM-DD HH:mm')))

        job = Job.save({
            'name': name,
            'status': 'pending',
            'message': data
        })

        registry = Registry()
        topic_arn = registry.get('topics').get('topic').get('migrationupload')
        conn = boto.sns.connect_to_region(registry.get('region').get('region'))

        try:
            conn.publish(topic_arn, str(job.uuid), name)
        except BotoServerError as e:
            log.error('Cannot publish Job=%s to Topic=%s', job.uuid, topic_arn)
            log.exception(e)
            return Response(status=500)
        except AttributeError as e:
            log.error('Cannot publish Job=%s to Topic=%s "%s"', job.uuid, topic_arn, str(e))
            return Response(status=500)

        return Response(response=json.dumps({
            'notify_msg': {
                'title': 'Job Added',
                'message': 'Migration job has been added. Upload will commence shortly.',
                'type': 'success'
            }}), content_type='application/json', status=200)

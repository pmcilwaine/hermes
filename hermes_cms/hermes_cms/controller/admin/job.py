# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import request, Response
from flask.views import MethodView
from hermes_cms.db import Job as JobDB
from sqlobject.sqlbuilder import DESC


class Job(MethodView):

    def get(self):
        """

        {
            "jobs": [
                {
                    "uuid": "",
                    "name": "",
                    "status": "",
                    "created": ""
                }
            ],
            "meta": {
                "offset": offset,
                "limit": limit
            }
        }

        :return:
        :rtype: flask.Response
        """

        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))

        items = []
        count = JobDB.select().count()
        for job in JobDB.select(orderBy=DESC(JobDB.q.created))[offset:limit]:
            items.append({
                'uuid': job.uuid,
                'name': job.name,
                'status': job.status.title(),
                'created': job.created.strftime('%Y-%m-%d %H:%M:%S'),
                'message': {k: v for k, v in job.message.iteritems() if k in ('download', 'content')}
            })

        return Response(response=json.dumps({
            'jobs': items,
            'meta': {
                'offset': offset,
                'limit': limit,
                'total': count
            }
        }), status=200, content_type='application/json')

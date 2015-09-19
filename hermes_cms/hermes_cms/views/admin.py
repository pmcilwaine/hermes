# /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from hermes_cms.core.auth import requires_permission, Auth
from flask import Blueprint, Response, request, json
from mako.lookup import TemplateLookup
from pkg_resources import resource_filename
from hermes_aws.s3 import S3
from hermes_cms.core.registry import Registry
from hermes_cms.helpers import common


log = logging.getLogger('hermes_cms.views.admin')
route = Blueprint('admin', __name__, url_prefix='/admin')
lookup = TemplateLookup(directories=[
    resource_filename('hermes_cms.templates.admin', '')
])


def url_rules():
    rules = Registry().get('admin_rules').get('rules')

    for admin_rule in rules:
        module = common.load_module_class(admin_rule['module_name'], admin_rule['class_name'])
        view = module.as_view(str(admin_rule['name']))

        _url_rules = admin_rule.get('urls')
        if not _url_rules:
            _url_rules = [{
                'url': admin_rule['url'],
                'methods': admin_rule['methods']
            }]

        for rule in _url_rules:
            route.add_url_rule(rule['url'], view_func=view, methods=rule['methods'])


@route.route('/', methods=['GET'])
@Auth.is_logged_in
@requires_permission(['list_document'])
def index():
    return Response(response=lookup.get_template('index.html').render(), status=200)


@route.route('/upload_url', methods=['POST'])
@Auth.is_logged_in
@requires_permission(['list_document'])
def sign_upload_url():
    registry = Registry()

    bucket = registry.get('storage')['bucket_name']
    signed_form = S3.generate_form(bucket, region=registry.get('region').get('region'))
    signed_form['file'] = {
        'bucket': bucket,
        'key': [item['value'] for item in signed_form['fields'] if item['name'] == 'key'].pop()
    }

    return Response(response=json.dumps(signed_form), content_type='application/json', status=201)


@route.route('/download_url', methods=['POST'])
@Auth.is_logged_in
@requires_permission(['list_document'])
def sign_download_url():
    data = request.json

    try:
        url = S3.generate_download_url(data.get('bucket'), data.get('key'))
        return Response(response=json.dumps({'url': url}), content_type='application/json', status=201)
    except (AttributeError, KeyError):
        return Response(response=json.dumps({}), content_type='application/json', status=400)

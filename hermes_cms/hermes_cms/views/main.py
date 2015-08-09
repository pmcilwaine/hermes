# /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import Blueprint, Response, json, request, redirect
from hermes_cms.core.auth import Auth
from hermes_cms.core.route import route as route_handler
from mako.lookup import TemplateLookup
from pkg_resources import resource_filename

log = logging.getLogger('hermes_cms.views.main')
route = Blueprint('main', __name__)
# todo this should be a configurable list of paths
lookup = TemplateLookup(directories=[
    resource_filename('hermes_cms.templates', '')
])


@route.route('/health')
def health():
    return Response(response=json.dumps({
        'status': 'ok'
    }), content_type='application/json', status=200)


@route.route('/login', methods=['GET'])
def get_login(error=None):
    status_code = 200 if not error else 400
    return Response(response=lookup.get_template('login.html').render(**dict(error=error)),
                    content_type='text/html', status=status_code)


@route.route('/login', methods=['POST'])
def post_login():

    user = Auth.get_by_login(request.form.get('email'), request.form.get('password'))
    if user:
        Auth.create_session(user)
        return redirect(request.args.get('next_page', '/'))

    return get_login(error={
        'message': 'Invalid email and/or password'
    })


@route.route('/logout', methods=['GET'])
def logout():
    if Auth.delete_session():
        return redirect('/')

    return Response(status=400)


@route.route('/', methods=['GET'], defaults={'path': 'index'})
@route.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def main_site(path=None):
    return route_handler(path)

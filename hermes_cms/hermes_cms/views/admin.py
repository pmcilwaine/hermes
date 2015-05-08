# /usr/bin/env python
# -*- coding: utf-8 -*-

from hermes_cms.core import Auth
from flask import Blueprint, Response, redirect
from mako.lookup import TemplateLookup
from pkg_resources import resource_filename

route = Blueprint('admin', __name__, url_prefix='/admin')
lookup = TemplateLookup(directories=[
    resource_filename('hermes_cms.templates.admin', '')
])


@route.route('/', methods=['GET'])
@Auth.is_logged_in
def index():
    return Response(response=lookup.get_template('index.html').render(), status=200)


@route.route('/logout', methods=['GET'])
def logout():
    if Auth.delete_session():
        return redirect('/')

    return Response(status=400)

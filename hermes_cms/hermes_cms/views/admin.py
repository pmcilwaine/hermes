# /usr/bin/env python
# -*- coding: utf-8 -*-

from hermes_cms.core import Auth
from flask import Blueprint, Response

route = Blueprint('admin', __name__, url_prefix='/admin')



@route.route('/', methods=['GET'])
@Auth.is_logged_in
def index():
    return Response(status=200)

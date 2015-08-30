# /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from flask import Flask, current_app, Response
from hermes_cms.core.registry import Registry
from hermes_cms.core.log import setup_logging
from sqlobject import sqlhub, connectionForURI

setup_logging()
log = logging.getLogger('hermes_cms.app')


def db_connect():
    database_url = current_app.config.get('DATABASE')
    if not database_url:
        database_url = str(Registry().get('database').get('database'))
    sqlhub.threadConnection = connectionForURI(database_url)


def db_close(resp):
    return resp


def create_app(app_name='hermes_cms', config_obj=None, blueprints=None):
    """

    :type app_name: str
    :param app_name:
    :type config_obj: object|None
    :param config_obj:
    :type blueprints: list|None
    :param blueprints:
    :return:
    """
    app = Flask(app_name)

    if config_obj:
        app.config.from_object(config_obj)
    else:
        # todo this needs to be in Configuration Registry
        app.secret_key = 'testing-key'

    blueprints = blueprints or Registry().get('blueprint').get('blueprint')

    for blueprint in blueprints:
        module = __import__(blueprint['name'], fromlist=blueprint['from'])
        route = getattr(module, blueprint['from'])
        if hasattr(module, 'url_rules'):
            module.url_rules()

        app.register_blueprint(route, **blueprint.get('kwargs', {}))

    def error_handler(error):
        log.exception(str(error))
        return Response(response=json.dumps({
            'notify_msg': {
                'title': 'Server Error',
                'message': 'An internal server error occurred.',
                'type': 'success'
            }
        }), content_type='application/json', status=500)

    app.register_error_handler(Exception, error_handler)
    app.before_request_funcs.setdefault(None, []).append(db_connect)
    app.after_request_funcs.setdefault(None, []).append(db_close)

    return app

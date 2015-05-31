# /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, current_app
from hermes_cms.core.registry import Registry
from hermes_cms.core.log import setup_logging
from sqlobject import sqlhub, connectionForURI

setup_logging()


def db_connect():
    database_url = current_app.config.get('DATABASE')
    if not database_url:
        database_url = Registry().get('database').get('database')
    sqlhub.threadConnection = connectionForURI(database_url)


def db_close(resp):
    if hasattr(sqlhub, 'threadConnection'):
        sqlhub.threadConnection.close()
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
        route = getattr(__import__(blueprint['name'], fromlist=blueprint['from']), blueprint['from'])
        app.register_blueprint(route, **blueprint.get('kwargs', {}))

    app.before_request_funcs.setdefault(None, []).append(db_connect)
    app.after_request_funcs.setdefault(None, []).append(db_close)

    return app

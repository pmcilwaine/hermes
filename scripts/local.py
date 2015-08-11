# /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sqlobject import connectionForURI, sqlhub
from hermes_cms.db import User, Document, Job
from hermes_cms.app import create_app
from flask import send_from_directory

"""
dbname – the database name (only in the dsn string)
database – the database name (only as keyword argument)
user – user name used to authenticate
password – password used to authenticate
host – database host address (defaults to UNIX socket if not provided)
port – connection port number (defaults to 5432 if not provided)
"""


class LocalConfig(object):
    DATABASE = 'sqlite://%s' % (os.path.abspath(os.path.join(os.path.dirname(__file__), 'database.db')), ) 
    SECRET_KEY = 'the_secret_key'

# setup application
sqlhub.threadConnection = connectionForURI(LocalConfig.DATABASE)
User.createTable(ifNotExists=True)
if not User.select().count():
    User(email='test@example.org', password='password', first_name='', last_name='', permissions='add_document,modify_document,delete_document,restore_deleted_document,restore_version_document,add_user,modify_user,delete_user,restore_user')

Document.createTable(ifNotExists=True)
Job.createTable(ifNotExists=True)
sqlhub.threadConnection.close()
# close for application to begin

app = create_app(config_obj=LocalConfig, blueprints=[
    {
        'name': 'hermes_cms.views.main',
        'from': 'route'
    },
    {
        'name': 'hermes_cms.views.admin',
        'from': 'route'
    }
])


@app.route('/assets/<path:filename>')
def public_static(filename):
    return send_from_directory(os.path.abspath('../hermes_ui/dist'), filename)


@app.route('/admin/analytics/')
def analytics_static():
    return 'Analytics page'


@app.route('/favicon.ico')
def favicon():
    return ''


app.run(debug=True)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from logging import config
from pkg_resources import resource_filename


def setup_logging():
    logging_dir = resource_filename('hermes_cms', 'data')
    _config = os.path.join(logging_dir, 'logging.ini')
    config.fileConfig(fname=_config)

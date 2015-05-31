#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from mock import MagicMock


def mock_modules():
    sys.modules['hermes_cms.core.log'] = MagicMock()

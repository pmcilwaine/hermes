# /usr/bin/env python
# -*- coding: utf-8 -*-
from wtforms import Form


class CustomForm(Form):

    def errors(self):
        """
        Returns a dictionary of errors with key being the field name and value the error message.

        :return:
        :rtype: dict
        """
        _errors = {}
        for name, field in self._fields.items():
            if field.errors:
                _errors[name] = field.errors.pop()

        return _errors

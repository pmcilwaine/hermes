# /usr/bin/env python
# -*- coding: utf-8 -*-
from wtforms import Form, StringField, validators, IntegerField


__all__ = ['Document']

class Document(object):

    def __init__(self, data=None):
        """

        :type data: dict
        :param data: A dictionary of fields to use.
        :return:
        """
        self.fields = data
        self._errors = {}

    def validate(self):
        """

        :rtype: bool
        """
        valid = True

        validate_document = DocumentForm(data=self.fields.get('document', {}))
        if not validate_document.validate():
            valid = False
            self._errors.update(validate_document.errors())

        return valid

    def errors(self):
        """
        Return the dictionary of errors. Should only be used after validate has been called and validate returns
        false.

        :rtype: dict
        """
        return self._errors

class DocumentForm(Form):
    gid = IntegerField()
    name = StringField(validators=[validators.DataRequired('Must enter the name of the document.')])
    url = StringField(validators=[validators.DataRequired('Must enter a URL')])
    type = StringField(validators=[validators.DataRequired('Must select a document type')])

    @staticmethod
    def validate_url(form, field):
        pass

    def errors(self):
        _errors = {}
        for name, field in self._fields.items():
            if field.errors:
                _errors[name] = field.errors.pop()

        return _errors

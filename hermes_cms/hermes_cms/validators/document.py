# /usr/bin/env python
# -*- coding: utf-8 -*-
import re
from sqlobject.sqlbuilder import IN
from hermes_cms.validators.customform import CustomForm
from hermes_cms.db.document import Document as DocumentDB
from wtforms import StringField, validators, IntegerField, ValidationError


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
        data = self.fields.get('document', {})
        if self.fields.get('id'):
            data['id'] = self.fields.get('id')

        validate_document = DocumentForm(data=data)
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


class DocumentForm(CustomForm):
    id = IntegerField()
    name = StringField(validators=[validators.DataRequired('Must enter the name of the document.')])
    url = StringField(validators=[validators.DataRequired('Must enter a URL')])
    type = StringField(validators=[validators.DataRequired('Must select a document type')])

    @staticmethod
    def validate_url(form, field):
        if DocumentDB.selectBy(url=field.data).filter(DocumentDB.q.id != form.id.data).count():
            raise ValidationError('URL is already in use')

        # check if multipage is a parent
        urls = [field.data]
        tmp_str = str(field.data)
        while tmp_str != '':
            tmp_str = '/'.join(tmp_str.split('/')[0:-1])
            if tmp_str:
                urls.append(tmp_str)

        query = (IN(DocumentDB.q.url, urls) & (DocumentDB.q.id != form.id.data) & (DocumentDB.q.type == 'MultiPage'))
        if DocumentDB.select(query).count():
            raise ValidationError('URL is already in use')

        if not re.match(r'^[a-z-0-9/]+$', field.data):
            raise ValidationError('Invalid URL. Cannot contain spaces')

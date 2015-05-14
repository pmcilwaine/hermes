# /usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import Form, StringField, PasswordField, validators, ValidationError
from hermes_cms.db import User as UserModel


class User(Form):
    uid = StringField('uid')

    email = StringField('email', validators=[
        validators.Email(message='Invalid Email'),
        validators.DataRequired(message='Email address is required')])

    password = PasswordField('password', validators=[
        validators.Length(min=6, max=36, message='Must enter a password')])

    first_name = StringField('first_name')
    last_name = StringField('last_name')

    @staticmethod
    def validate_email(form, field):
        """

        :param form:
        :param field:
        :return:
        """
        if UserModel.selectBy(email=field.data).filter(UserModel.q.uid != form.uid.data).getOne(None):
            raise ValidationError('Email address already in use')

        return True

    def errors(self):
        """
        Returns all the errors messages as a dictionary.

        :rtype: dict
        """
        _errors = {}
        for name, field in self._fields.items():
            if field.errors:
                _errors[name] = field.errors.pop()

        return _errors

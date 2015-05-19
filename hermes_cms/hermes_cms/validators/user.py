# /usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import StringField, PasswordField, validators, ValidationError
from hermes_cms.db import User as UserModel
from hermes_cms.validators.customform import CustomForm


class User(CustomForm):
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

# /usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import StringField, PasswordField, validators, ValidationError
from hermes_cms.db import User as UserModel
from hermes_cms.validators.customform import CustomForm


class User(CustomForm):
    id = StringField('id')

    email = StringField('email', validators=[
        validators.Email(message='Invalid Email'),
        validators.DataRequired(message='Email address is required')])

    password = PasswordField('password', validators=[])

    first_name = StringField('first_name')
    last_name = StringField('last_name')

    @staticmethod
    def validate_email(form, field):
        """

        :param form:
        :param field:
        :return:
        """
        if UserModel.selectBy(email=field.data).filter(UserModel.q.id != form.id.data).getOne(None):
            raise ValidationError('Email address already in use')

        return True

    @staticmethod
    def validate_password(form, field):
        user_record = UserModel.selectBy(email=form.email.data).filter(UserModel.q.id == form.id.data).getOne(None)
        if user_record and not field.data:
            return True

        validators.Length(min=6, max=36, message='Must enter a password')(form, field)

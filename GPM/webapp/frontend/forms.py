# -*- coding: utf-8 -*-

from flask import Markup

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import (HiddenField, BooleanField, TextField,
        PasswordField, SubmitField)
from flask.ext.wtf import Required, Length, EqualTo, Email
from flask.ext.wtf.html5 import EmailField

from ..user import User
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, 
        USERNAME_LEN_MIN, USERNAME_LEN_MAX)


class LoginForm(Form):
    next = HiddenField()
    login = TextField(u'Nombre de Usuario', [Required()])
    password = PasswordField('Contraseña', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    submit = SubmitField('Ingresar')


class SignupForm(Form):
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()],
            description=u"Cuál es tu dirección de email?")
    password = PasswordField(u'Contraseña', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s caracteres o más!' % PASSWORD_LEN_MIN)
    name = TextField(u'Elija su nombre de Usuario', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Puede cambiarlo luego.")
    submit = SubmitField('Sign up')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'El Nombre de Usuario ya existe')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'El email ya existe')

class RecoverPasswordForm(Form):
    email = EmailField(u'Your email', [Email()])
    submit = SubmitField('Send instructions')


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField(u'Password', [Required()])
    password_again = PasswordField(u'Password again', [EqualTo('password', message="Las contraseñas no coinciden")]) 
    submit = SubmitField('Guardar')


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    submit = SubmitField('Reauthenticate')

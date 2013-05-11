# -*- coding: utf-8 -*-

from flask import Markup

from flask_wtf import Form, ValidationError
from flask_wtf import (HiddenField, BooleanField, TextField,
        PasswordField, SubmitField)
from flask_wtf import Required, Length, EqualTo, Email
from flask_wtf.html5 import EmailField

from ..modelos import User
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
            description=u"Cuál es tu dirección de correo?")
    password = PasswordField(u'Contraseña', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s caracteres o más!' % PASSWORD_LEN_MIN)
    name = TextField(u'Nombre de usuario', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    agree = BooleanField(u'Agree to the ' + 
        Markup('<a target="blank" href="/terms">Terms of Servic</a>'), [Required()])
    submit = SubmitField('Registrarse')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'Nombre de usuario en uso')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'Email ya está en uso')


class RecoverPasswordForm(Form):
    email = EmailField(u'Your email', [Email()])
    submit = SubmitField('Send instructions')


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField(u'Contraseña', [Required()])
    password_again = PasswordField(u'Contraseña nuevamente', [EqualTo('password', message="Contraseñas no coinciden")]) 
    submit = SubmitField('Guardar')


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(u'Contraseña', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    submit = SubmitField('Reautenticar')

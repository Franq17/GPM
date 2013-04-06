# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import HiddenField, SubmitField, RadioField, DateField
from flask.ext.wtf import AnyOf

from ..user import USER_ROLE, USER_STATUS

from flask.ext.wtf.html5 import EmailField
from flask.ext.wtf import Required, Length, EqualTo, Email
from flask.ext.wtf import (HiddenField, BooleanField, TextField,
        PasswordField, SubmitField)
from ..user import User
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, 
        USERNAME_LEN_MIN, USERNAME_LEN_MAX)      

class UserForm(Form):
    next = HiddenField()
    role_id = RadioField(u"Rol", [AnyOf([str(val) for val in USER_ROLE.keys()])],
            choices=[(str(val), label) for val, label in USER_ROLE.items()])
    status_id = RadioField(u"Status", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Fecha de Creación')
    submit = SubmitField(u'Guardar')

class DeleteUserForm(Form):
    next = HiddenField()
    role_id = RadioField(u"Rol", [AnyOf([str(val) for val in USER_ROLE.keys()])],
            choices=[(str(val), label) for val, label in USER_ROLE.items()])
    status_id = RadioField(u"Status", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Fecha de Creación')
    submit = SubmitField(u'Eliminar')

class CreateUserForm(Form):
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()])
    password = PasswordField(u'Contraseña', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s caracteres o más!' % PASSWORD_LEN_MIN)
    name = TextField(u'Nombre de Usuario', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    submit = SubmitField(u'Crear')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'El nombre de Usuario ya existe')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'El email ya existe')

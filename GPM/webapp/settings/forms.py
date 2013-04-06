# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import (HiddenField, TextField,
        PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
        FileField, DecimalField, DateField)
from flask.ext.wtf import (Required, Length, EqualTo, Email, AnyOf,
        NumberRange, URL, Optional)
from flask.ext.wtf.html5 import EmailField, TelField, IntegerField
from flask.ext.login import current_user

from ..user import User, USER_ROLE, USER_STATUS
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX,
		NAME_LEN_MIN, NAME_LEN_MAX)


class ProfileForm(Form):
    next = HiddenField()
    
    nameReal = TextField(u'Nombre', [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)])
    
    apellido = TextField(u'Apellido', [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)])
    name = TextField(u'Nombre de Usuario', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u'Combinación de letras/dígitos/guiones, con al menos %s caracteres.' % USERNAME_LEN_MIN)
    email = EmailField(u'Email', [Required(), Email()])
    # Don't use the same name as model because we are going to use populate_obj().
    avatar_file = FileField(u"Avatar", [Optional()])
    document = IntegerField(u'Número de Documento',[Required()])
    
    phone = TelField(u'Teléfono', [Optional(), Length(max=64)])
    location = TextField(u'Dirección', [Optional(), Length(max=64)])
    descripcion = TextAreaField(u'Descripción', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Guardar')


class PasswordForm(Form):
    next = HiddenField()
    password = PasswordField('Contraseña', [Required()])
    new_password = PasswordField('Nueva contraseña', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField('Contraseña nuevamente', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
    submit = SubmitField(u'Guardar')

    def validate_password(form, field):
        user = User.query.filter_by(name=current_user.name).first()
        if not user.check_password(field.data):
            raise ValidationError("Contraseña incorrecta.")

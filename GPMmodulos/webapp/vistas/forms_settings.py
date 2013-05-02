# -*- coding: utf-8 -*-

from flask_wtf import Form, ValidationError
from flask_wtf import (HiddenField, TextField,
        PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
        FileField, DecimalField, DateField)
from flask_wtf import (Required, Length, EqualTo, Email, AnyOf,
        NumberRange, URL, Optional)
from flask_wtf.html5 import URLField, EmailField, TelField
from flask_login import current_user

from ..modelos import User, USER_ROLE, USER_STATUS
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX,
        AGE_MIN, AGE_MAX, DEPOSIT_MIN, DEPOSIT_MAX)


class ProfileForm(Form):
    next = HiddenField()
    name = TextField(u'Nombre de Usuario', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
            #description=u'Combination of letters/digits/underscore, at least %s characters.' % USERNAME_LEN_MIN)
    nombre = TextField(u'Nombre', [Optional(), Length(max=64)])
    apellido = TextField(u'Apellido', [Optional(), Length(max=64)])
    email = EmailField(u'Email', [Required(), Email()])
    telefono = TextField(u'Telefono', [Optional(), Length(max=64)])
    ci = TextField(u'CI', [Optional(), Length(max=64)])
    # Don't use the same name as model because we are going to use populate_obj().
    avatar_file = FileField(u"Avatar", [Optional()])
    #age = IntegerField(u'Age', [Optional(), NumberRange(AGE_MIN, AGE_MAX)])
    #phone = TelField(u'Phone', [Optional(), Length(max=64)])
    #url = URLField(u'URL', [Optional(), URL()])
    #deposit = DecimalField(u'Deposit', [Optional(), NumberRange(DEPOSIT_MIN, DEPOSIT_MAX)])
    #location = TextField(u'Location', [Optional(), Length(max=64)])
    #bio = TextAreaField(u'Bio', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Guardar')


class PasswordForm(Form):
    next = HiddenField()
    password = PasswordField('Contraseña', [Required()])
    new_password = PasswordField('Nueva Contraseña', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField('Contraseña de nuevo', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
    submit = SubmitField(u'Guardar')

    def validate_password(form, field):
        user = User.query.filter_by(name=current_user.name).first()
        if not user.check_password(field.data):
            raise ValidationError("Contraseña incorrecta.")

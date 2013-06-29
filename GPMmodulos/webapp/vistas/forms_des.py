# -*- coding: utf-8 -*-

from flask_wtf import Form, ValidationError
from flask_wtf import HiddenField, SubmitField, RadioField, DateField
from flask_wtf import AnyOf

from ..modelos import USER_STATUS, PROYECTO_ESTADOS, COMITE_ESTADOS,LINEABASE_ESTADOS

from flask_wtf.html5 import EmailField
from flask_wtf import Required, Optional, Length, EqualTo, Email
from flask_wtf import (HiddenField, BooleanField, TextField, TextAreaField,
                       PasswordField, IntegerField, SelectField, SelectMultipleField, SubmitField)
from ..modelos import User, Proyecto, Comite, TipoItem, Fase, Atributo, Rol

from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, 
        USERNAME_LEN_MIN, USERNAME_LEN_MAX, REALNAME_LEN_MIN, REALNAME_LEN_MAX)      

#ITEM

class CrearItemForm(Form):
    next = HiddenField()
    nombre = nombre = TextField(u'Nombre del Item', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    tipoItem_id = SelectField(u'TipoItemID', coerce=int,)
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Crear')

class ItemForm(Form):
    next = HiddenField()
    nombre = nombre = TextField(u'Nombre del Item', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Editar')

# -*- coding: utf-8 -*-

from flask_wtf import Form, ValidationError
from flask_wtf import HiddenField, SubmitField, RadioField, DateField
from flask_wtf import AnyOf

from ..modelos import COMITE_ESTADOS, LINEABASE_ESTADOS

from flask_wtf.html5 import EmailField
from flask_wtf import Required, Optional, Length, EqualTo, Email
from flask_wtf import (HiddenField, BooleanField, TextField, TextAreaField,
                       PasswordField, IntegerField, SelectField, SelectMultipleField, SubmitField)
from ..modelos import Comite

from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, 
        USERNAME_LEN_MIN, USERNAME_LEN_MAX, REALNAME_LEN_MIN, REALNAME_LEN_MAX)      


#LINEA BASE

#COMITE
class ComiteForm(Form):
    next = HiddenField()
    descripcion = TextAreaField(u'Descripcion', [Optional(),Length(max=1024)])
    submit = SubmitField(u'Guardar')
    
class CrearComiteForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre de Comite', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    proyecto_id = SelectField(u'ProyectoID', coerce=int,)
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Crear')
    
    def validate_nombre(self, field):
        if Comite.query.filter_by(nombre=field.data).first() is not None:
            raise ValidationError(u'El nombre del Comite ya existe')
    
class BorrarComiteForm(Form):
    next = HiddenField()
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    # A demo of datepicker.
    submit = SubmitField(u'Eliminar')
    
class UserxComiteForm(Form):
    next = HiddenField()
    # A demo of datepicker.
    usuarioPorComite = SelectMultipleField(u'Usuarios' ,coerce=int)
    submit = SubmitField(u'Agregar Miembro')

class CrearLBForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre de Linea de Base', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    submit = SubmitField(u'Crear')

class AsignarItemsLBForm(Form):
    next = HiddenField()
    items = SelectMultipleField(u'Seleccione Items' ,coerce=int)
    submit = SubmitField(u'Agregar')
    
class LineaBaseForm(Form):
    next = HiddenField()
    numero_lb = IntegerField(u'Numero de Linea Base',[Required()])
    estado = RadioField(u"Estados", [AnyOf([str(val) for val in LINEABASE_ESTADOS.keys()])],
            choices=[(str(val), label) for val, label in LINEABASE_ESTADOS.items()])
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Editar')

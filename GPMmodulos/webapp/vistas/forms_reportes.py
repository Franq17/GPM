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

class ReporteItemsxProyectoForm(Form):
    next = HiddenField()
    proyecto_id = SelectField(u'Seleccione un Proyecto:', coerce=int,)
    submit = SubmitField(u'Crear Reporte')
    
class ReporteHistorialxItemForm(Form):      
    next = HiddenField()
    proyecto_id = SelectField(u'Seleccione un Proyecto:', coerce=int,)
    submit = SubmitField(u'Crear Reporte')
    
# -*- coding: utf-8 -*-

from flask_wtf import Form, ValidationError
from flask_wtf import HiddenField, SubmitField, RadioField, DateField
from flask_wtf import AnyOf

from ..modelos import USER_ROLE, USER_STATUS, PROYECTO_ESTADOS, COMITE_ESTADOS

from flask_wtf.html5 import EmailField, SearchField
from flask_wtf import Required, Optional, Length, EqualTo, Email
from flask_wtf import (HiddenField, BooleanField, TextField, TextAreaField,
                       PasswordField, IntegerField, SelectField, SelectMultipleField, SubmitField)
from ..modelos import User, Proyecto, Comite
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, 
        USERNAME_LEN_MIN, USERNAME_LEN_MAX, REALNAME_LEN_MIN, REALNAME_LEN_MAX)      


#USER
class UserForm(Form):
    next = HiddenField()
    status_id = RadioField(u"Estados", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Fecha de Creación')
    submit = SubmitField(u'Guardar')

class DeleteUserForm(Form):
    next = HiddenField()
    status_id = RadioField(u"Estados", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Fecha de Creación')
    submit = SubmitField(u'Eliminar')

class CreateUserForm(Form):
    next = HiddenField()
    email = EmailField(u'Email', [Email()])
    password = PasswordField(u'Contraseña', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    name = TextField(u'Nombre de Usuario', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    rolPorUsuario = SelectMultipleField(u'Roles', [Required()], coerce=int)
    submit = SubmitField('Crear')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'Nombre de usuario en uso')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'Email en uso')

class SearchUserForm(Form):
    next = HiddenField()
    name = SearchField(u'Nombre de Usuario')
    submit = SubmitField(u'Buscar')

#PROYECTO
class ProyectoForm(Form):
    next = HiddenField()
    
    estado_id = RadioField(u"Estados", [AnyOf([str(val) for val in PROYECTO_ESTADOS.keys()])],
            choices=[(str(val), label) for val, label in PROYECTO_ESTADOS.items()])
    descripcion = TextAreaField(u'Descripción', [Optional(), Length(max=1024)])
    
    submit = SubmitField(u'Guardar')

class BorrarProyectoForm(Form):
    next = HiddenField()
    estado_id = RadioField(u"Estados", [AnyOf([str(val) for val in PROYECTO_ESTADOS.keys()])],
            choices=[(str(val), label) for val, label in PROYECTO_ESTADOS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Fecha de Creación')
    
    submit = SubmitField(u'Eliminar')

class CrearProyectoForm(Form):
    next = HiddenField()

    nombre = TextField(u'Nombre del Proyecto', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    numero_fases = IntegerField(u'Número de fases',[Required()])
    lider_proyecto = SelectField(u'Líder de Proyecto',coerce=int,)
    descripcion = TextAreaField(u'Descripción', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Crear')

    def validate_name(self, field):
        if Proyecto.query.filter_by(nombre=field.data).first() is not None:
            raise ValidationError(u'El nombre del Proyecto ya existe')

class BuscarProyectoForm(Form):
    next = HiddenField()
    nombre = SearchField(u'Nombre del Proyecto', [Required()])
    submit = SubmitField(u'Buscar')
    
#COMITE
class ComiteForm(Form):
    next = HiddenField()
    descripcion = TextAreaField(u'Descripción', [Optional(),Length(max=1024)])
    submit = SubmitField(u'Guardar')
    
class CrearComiteForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre de Comité', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    proyecto_id = SelectField(u'ProyectoID', coerce=int,)
    descripcion = TextAreaField(u'Descripción', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Crear')
    
    def validate_name(self, field):
        if Comite.query.filter_by(nombre=field.data).first() is not None:
            raise ValidationError(u'El nombre del Comité ya existe')
    
class BorrarComiteForm(Form):
    next = HiddenField()
    descripcion = TextAreaField(u'Descripción', [Optional(), Length(max=1024)])
    # A demo of datepicker.
    submit = SubmitField(u'Eliminar')
    
class BuscarComiteForm(Form):
    next = HiddenField()
    nombre = SearchField(u'Nombre de Comité', [Required()])
    submit = SubmitField(u'Buscar')

#ROL
class CrearRolForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre del Rol', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    descripcion = TextAreaField(u'Descripción', [Optional(), Length(max=1024)])
    permisoPorRol = SelectMultipleField(u'Permisos', [Required()], coerce=int)
    submit = SubmitField(u'Crear')
    
    def validate_name(self, field):
        if Rol.query.filter_by(nombre=field.data).first() is not None:
            raise ValidationError(u'El nombre del Rol ya existe')

class BorrarRolForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre del Rol', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    descripcion = TextAreaField(u'Descripción', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Eliminar')

class RolForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre del Rol', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    descripcion = TextAreaField(u'Descripción', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Editar')


class BuscarRolForm(Form):
    next = HiddenField()
    nombre = SearchField(u'Nombre del Rol')
    
#RELACIONES

class UserxComiteForm(Form):
    next = HiddenField()
    # A demo of datepicker.
    usuarioPorComite = SelectMultipleField(u'Usuarios' ,coerce=int)
    submit = SubmitField(u'Agregar Miembro')
    
class PermisoxRolForm(Form):
    next = HiddenField()
    permisoPorRol = SelectMultipleField(u'Permisos' ,coerce=int)
    submit = SubmitField(u'Guardar')
    
class RolxUsuarioForm(Form):
    next = HiddenField()
    rolPorUsuario = SelectMultipleField(u'Roles' ,coerce=int)
    submit = SubmitField(u'Guardar')

# -*- coding: utf-8 -*-

from flask_wtf import Form, ValidationError
from flask_wtf import HiddenField, SubmitField, RadioField, DateField
from flask_wtf import AnyOf

from ..modelos import USER_ROLE, USER_STATUS, PROYECTO_ESTADOS, COMITE_ESTADOS,LINEABASE_ESTADOS

from flask_wtf.html5 import EmailField
from flask_wtf import Required, Optional, Length, EqualTo, Email
from flask_wtf import (HiddenField, BooleanField, TextField, TextAreaField,
                       PasswordField, IntegerField, SelectField, SelectMultipleField, SubmitField)
from ..modelos import User, Proyecto, Comite, TipoItem, Fase, Atributo, Rol

from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, 
        USERNAME_LEN_MIN, USERNAME_LEN_MAX, REALNAME_LEN_MIN, REALNAME_LEN_MAX)      


#USER
class UserForm(Form):
    next = HiddenField()
    status_id = RadioField(u"Estados", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Fecha de Creacion')
    submit = SubmitField(u'Guardar')

class DeleteUserForm(Form):
    next = HiddenField()
    status_id = RadioField(u"Estados", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Fecha de Creacion')
    submit = SubmitField(u'Eliminar')

class CreateUserForm(Form):
    next = HiddenField()
    email = EmailField(u'Email', [Email()])
    password = PasswordField(u'Contrasenha', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    name = TextField(u'Nombre de Usuario', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    rolPorUsuario = SelectMultipleField(u'Roles', [Required()], coerce=int)
    submit = SubmitField('Crear')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'Nombre de usuario en uso')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'Email en uso')

#PROYECTO
class ProyectoForm(Form):
    next = HiddenField()
    estado_id = RadioField(u"Estados", [AnyOf([str(val) for val in PROYECTO_ESTADOS.keys()])],
            choices=[(str(val), label) for val, label in PROYECTO_ESTADOS.items()])
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Guardar')
    

class BorrarProyectoForm(Form):
    next = HiddenField()
    estado_id = RadioField(u"Estados", [AnyOf([str(val) for val in PROYECTO_ESTADOS.keys()])],
            choices=[(str(val), label) for val, label in PROYECTO_ESTADOS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Fecha de Creacion')
    submit = SubmitField(u'Eliminar')

class CrearProyectoForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre del Proyecto', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    numero_fases = IntegerField(u'Numero de fases',[Required()])
    lider_proyecto = SelectField(u'Lider de Proyecto',coerce=int,)
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Crear')

    def validate_nombre(self, field):
        if Proyecto.query.filter_by(nombre=field.data).first() is not None:
            raise ValidationError(u'El nombre del Proyecto ya existe')
    
    def validate_numero_fases(self,field):
        if field.data < 0 or field.data > 3:
            raise ValidationError(u'Numero de fases de un proyecto no valido')
          
#COMITE
#class ComiteForm(Form):
#    next = HiddenField()
#    descripcion = TextAreaField(u'Descripcion', [Optional(),Length(max=1024)])
#    submit = SubmitField(u'Guardar')
#    
#class CrearComiteForm(Form):
#    next = HiddenField()
#    nombre = TextField(u'Nombre de Comite', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
#    proyecto_id = SelectField(u'ProyectoID', coerce=int,)
#    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
#    submit = SubmitField(u'Crear')
#    
#    def validate_nombre(self, field):
#        if Comite.query.filter_by(nombre=field.data).first() is not None:
#            raise ValidationError(u'El nombre del Comite ya existe')
#    
#class BorrarComiteForm(Form):
#    next = HiddenField()
#    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
#    # A demo of datepicker.
#    submit = SubmitField(u'Eliminar')
    
#ROL

class CrearRolForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre del Rol', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    permisoPorRol = SelectMultipleField(u'Permisos', [Required()], coerce=int)
    submit = SubmitField(u'Crear')
    
    def validate_nombre(self, field):
        if Rol.query.filter_by(nombre=field.data).first() is not None:
            raise ValidationError(u'El nombre del Rol ya existe')

class BorrarRolForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre del Rol', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Eliminar')

class RolForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre del Rol', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Editar')

#FASE

class CrearFaseForm(Form):
    next = HiddenField()
    nombre = nombre = TextField(u'Nombre de Fase', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Crear')
    
    def validate_nombre(self, field):
        if Fase.query.filter_by(nombre=field.data).first() is not None:
            raise ValidationError(u'El nombre de la Fase ya existe')
    
class FaseForm(Form):
    next = HiddenField()
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Editar')
     
#TIPO DE ITEM
class CrearTipoItemForm(Form):
    next = HiddenField()
    nombre = nombre = TextField(u'Nombre de Tipo de Item', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Crear')
    
    def validate_nombre(self, field):
        if TipoItem.query.filter_by(nombre=field.data).first() is not None:
            raise ValidationError(u'El nombre del tipo de Item ya existe')

class TipoItemForm(Form):
    next = HiddenField()
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Editar')

class CrearAtributoForm(Form):
    next = HiddenField()
    nombre = TextField(u'Nombre de Atributo', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
    atributo_id = SelectField(u'AtributoID', [Optional()], coerce=int)
    valor = TextField(u'Valor', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Crear')
    
    def validate_nombre(self, field):
        if Atributo.query.filter_by(nombre=field.data).first() is not None:
            raise ValidationError(u'El nombre del Atributo ya existe')


####################################################################################    
#RELACIONES

class UserxComiteForm(Form):
    next = HiddenField()
    # A demo of datepicker.
    usuarioPorComite = SelectMultipleField(u'Usuarios' ,coerce=int)
    submit = SubmitField(u'Agregar Miembro')
    
class PermisoxRolForm(Form):
    next = HiddenField()
    permisoPorRol = SelectMultipleField(u'Permisos' ,coerce=int, option_widget=None)
    submit = SubmitField(u'Guardar')
    
class RolxUsuarioForm(Form):
    next = HiddenField()
    rolPorUsuario = SelectMultipleField(u'Roles' ,coerce=int)
    submit = SubmitField(u'Guardar')
    
class UsuarioxProyectoForm(Form):
    next = HiddenField()
    usuarioPorProyecto = SelectMultipleField(u'Usuarios', coerce=int)
    submit = SubmitField(u'Agregar')
    
class RolxProyectoForm(Form):
    next = HiddenField()
    roles = SelectMultipleField(u'Roles', coerce=int)
    submit = SubmitField(u'Agregar')

#class CrearItemForm(Form):
#    next = HiddenField()
#    nombre = nombre = TextField(u'Nombre del Item', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
#    tipoItem_id = SelectField(u'TipoItemID', coerce=int,)
#    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
#    submit = SubmitField(u'Crear')
#
#class ItemForm(Form):
#    next = HiddenField()
#    nombre = nombre = TextField(u'Nombre del Item', [Required(), Length(REALNAME_LEN_MIN, REALNAME_LEN_MAX)])
#    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
#    submit = SubmitField(u'Editar')

class CrearLineaBaseForm(Form):
    next = HiddenField()
    numero_lb = IntegerField(u'Numero de Linea Base',[Required()])
    fase_id = SelectField(u'FaseID', coerce=int,)
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Crear')

class LineaBaseForm(Form):
    next = HiddenField()
    numero_lb = IntegerField(u'Numero de Linea Base',[Required()])
    estado = RadioField(u"Estados", [AnyOf([str(val) for val in LINEABASE_ESTADOS.keys()])],
            choices=[(str(val), label) for val, label in LINEABASE_ESTADOS.items()])
    descripcion = TextAreaField(u'Descripcion', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Editar')


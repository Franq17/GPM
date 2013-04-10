# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import HiddenField, SubmitField, RadioField, DateField
from flask.ext.wtf import AnyOf

from ..user import USER_ROLE, USER_STATUS
from ..project import PROJECT_STATUS


from flask.ext.wtf.html5 import EmailField
from flask.ext.wtf import Required, Length, EqualTo, Email, Optional
from flask.ext.wtf import (HiddenField, BooleanField, TextField,
                           TextAreaField, PasswordField, IntegerField, SubmitField)

from ..user import User
from ..project import Project

from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, 
        USERNAME_LEN_MIN, USERNAME_LEN_MAX)      

class UserForm(Form):
    next = HiddenField()
    role_id = RadioField(u"Rol", [AnyOf([str(val) for val in USER_ROLE.keys()])],
            choices=[(str(val), label) for val, label in USER_ROLE.items()])
    status_id = RadioField(u"Status", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
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

class SearchUserForm(Form):
    next = HiddenField()
    name = TextField(u'Nombre de Usuario', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    submit = SubmitField(u'Buscar')
    

class ProjectForm(Form):
    next = HiddenField()
    
    estado_id = RadioField(u"Status", [AnyOf([str(val) for val in PROJECT_STATUS.keys()])],
            choices=[(str(val), label) for val, label in PROJECT_STATUS.items()])
    descripcion = TextAreaField(u'Descripción', [Optional(), Length(max=1024)])
    
    submit = SubmitField(u'Guardar')

class DeleteProjectForm(Form):
    next = HiddenField()
    
    estado_id = RadioField(u"Status", [AnyOf([str(val) for val in PROJECT_STATUS.keys()])],
            choices=[(str(val), label) for val, label in PROJECT_STATUS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Fecha de Creación')
    submit = SubmitField(u'Eliminar')

class CreateProjectForm(Form):
    next = HiddenField()

    nombre = TextField(u'Nombre del Proyecto', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    numero_fases = IntegerField(u'Número de fases',[Required()])
    lider_proyecto = TextField(u'Líder de Proyecto', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    descripcion = TextAreaField(u'Descripción', [Optional(), Length(max=1024)])
    submit = SubmitField(u'Crear')

    def validate_name(self, field):
        if Project.query.filter_by(nombre=field.data).first() is not None:
            raise ValidationError(u'El nombre del Proyecto ya existe')

class SearchProjectForm(Form):
    next = HiddenField()
    name = TextField(u'Nombre del Proyecto', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    submit = SubmitField(u'Buscar')
    



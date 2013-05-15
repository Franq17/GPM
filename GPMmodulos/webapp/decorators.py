# -*- coding: utf-8 -*-

from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role_id != 0:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
#1
def crearUsuarios_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('crearUsuarios') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
#2
def modificarUsuarios_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('modificarUsuarios') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#3
def eliminarUsuarios_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('eliminarUsuarios') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#4
def verUsuarios_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('verUsuarios') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
#5
def crearRoles_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('crearRoles') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
#6
def modificarRoles_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('modificarRoles') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#7
def eliminarRoles_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('eliminarRoles') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#8
def verRoles_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('verRoles') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#9
def verPermisos_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('verPermisos') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


#10
def crearProyectos_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('crearProyectos') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
#11
def modificarProyectos_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('modificarProyectos') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#12
def eliminarProyectos_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('eliminarProyectos') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#13
def verProyectos_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('verProyectos') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#14
def crearComites_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('crearComites') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#15
def modificarComites_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('modificarComites') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#16
def eliminarComites_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('eliminarComites') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#17
def verComites_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('verComites') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#18
def verMiembrosComites_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('verMiembrosComites') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#19
def crearItems_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('crearItems') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
#20
def modificarItems_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('modificarItems') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#21
def eliminarItems_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('eliminarItems') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#22
def verItems_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('verItems') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#23
def crearFases_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('crearFases') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
#24
def modificarFases_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('modificarFases') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#25
def eliminarFases_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('eliminarFases') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#26
def verFases_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.comprobarPermiso('verFases') == False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


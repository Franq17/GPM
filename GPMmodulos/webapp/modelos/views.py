# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, current_app, redirect, url_for, send_from_directory, flash
from flask_login import login_required, current_user

from .models_adm import User, Rol, Proyecto, Comite, TipoItem, Solicitud
from .constants import DEFAULT_USER_AVATAR

user = Blueprint('user', __name__, url_prefix='/user')
rol = Blueprint('rol', __name__, url_prefix='/rol')
proyecto = Blueprint('proyecto', __name__, url_prefix='/proyecto')
comite = Blueprint('comite', __name__, url_prefix='/comite')
tipoItem = Blueprint('tipoItem', __name__, url_prefix='/tipoItem')

@user.route('/')
@user.route('/<numSolicitud>')
@login_required
def index(id_solicitud=None, numSolicitud=None):
    if id_solicitud is not None:
        solicitud = Solicitud.query.filter_by(id=id_solicitud).first_or_404()
    else:
        solicitud = None

    return render_template('index/indexUser.html', current_user=current_user, solicitud=solicitud, numSolicitud=numSolicitud)

@user.route('/<name>')
def pub(name):
#    if current_user.is_authenticated() and current_user.name == name:
#        return redirect(url_for('user.index'))
    user = User.query.filter_by(name=name).first_or_404()
    return render_template('index/showUser.html', user=user)

@rol.route('/rol')
@rol.route('/rol/<nombre>')
def pubRol(nombre):
    rol = Rol.query.filter_by(nombre=nombre).first_or_404()
    return render_template('index/showRol.html', rol=rol)

@proyecto.route('/proyecto')
@proyecto.route('/proyecto/<nombre>')
def pubProyecto(nombre):
    proyecto = Proyecto.query.filter_by(nombre=nombre).first_or_404()
    return render_template('index/showProyecto.html', proyecto=proyecto)

@comite.route('/comite')
@comite.route('/comite/<nombre>')
def pubComite(nombre):    
    comite = Comite.query.filter_by(nombre=nombre).first_or_404()
    return render_template('index/showComite.html', comite=comite)

@tipoItem.route('/tipoItem')
@tipoItem.route('/tipoItem/<nombre>')
def pubTipoItem(nombre):    
    tipoItem = TipoItem.query.filter_by(nombre=nombre).first_or_404()
    return render_template('index/showTipoItem.html', tipoItem=tipoItem)

@user.route('/avatar')
@user.route('/avatar/<path:avatar_filename>')
def avatar(avatar_filename=None):
    if avatar_filename is None:
        avatar_filename = DEFAULT_USER_AVATAR
    return send_from_directory(current_app.config['USER_AVATAR_UPLOAD_FOLDER'], avatar_filename)

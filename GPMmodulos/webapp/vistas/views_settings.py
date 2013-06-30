# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, current_app, request, flash
from flask_login import login_required, current_user

from ..extensions import db
from ..modelos import User
from ..utils import allowed_file, id_generator, ALLOWED_AVATAR_EXTENSIONS
from .forms_settings import ProfileForm, PasswordForm


settings = Blueprint('settings', __name__, url_prefix='/settings')


@settings.route('/profile', methods=['GET', 'POST'])
@login_required
def perfil():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = ProfileForm(#obj=user.user_detail, 
            name=current_user.name,
            email=current_user.email,
            status_id=current_user.status_id, nombre=current_user.nombre,
            apellido=current_user.apellido, telefono=current_user.telefono,
            ci=current_user.ci, next=request.args.get('next'))

    if form.validate_on_submit():

        if form.avatar_file.data:
            file = request.files[form.avatar_file.name]
            if file and allowed_file(file.filename):
                # Don't trust any input, we use a random string as filename.
                # or use secure_filename:
                # http://flask.pocoo.org/docs/patterns/fileuploads/
                user_avatar_folder = os.path.join(
                        current_app.config['USER_AVATAR_UPLOAD_FOLDER'],
                        str(user.id))
                if not os.path.exists(user_avatar_folder):
                    os.mkdir(user_avatar_folder)
                random_id = id_generator()
                file.save(os.path.join(user_avatar_folder, random_id))
                if user.avatar:
                    os.remove(os.path.join(
                        current_app.config['USER_AVATAR_UPLOAD_FOLDER'],
                        user.avatar))
                user.avatar = os.path.join(str(user.id), random_id)
            else:
                form.avatar_file.errors.append(
                        u"Only accept files with following extensions: %s" %
                        '/'.join(ALLOWED_AVATAR_EXTENSIONS))

        form.populate_obj(user)
        #form.populate_obj(user.user_detail)

        db.session.add(user)
        db.session.commit()

        flash('Perfil actualizado', 'success')

    return render_template('settings/profile.html', user=user,
            active="perfil", form=form)


@settings.route('/password', methods=['GET', 'POST'])
@login_required
def contrasena():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = PasswordForm(next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)
        user.password = form.new_password.data

        db.session.add(user)
        db.session.commit()

        flash('Contrasena modificada', 'success')

    return render_template('settings/password.html', user=user,
            active="contrasena", form=form)

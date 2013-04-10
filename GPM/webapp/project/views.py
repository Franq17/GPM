# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, current_app, redirect, url_for, send_from_directory
from flask.ext.login import login_required 

from .models import Project

project = Blueprint('project', __name__, url_prefix='/project')

@project.route('/')
@login_required
def index():
    return render_template('project/index.html')

@project.route('/<name>')
@login_required
def pub(name):
    if project.nombre == name:
        return redirect(url_for('project.index'))

    project = Project.query.filter_by(nombre=name).first_or_404()
    return render_template('project/show.html', project=project)

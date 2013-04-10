# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask.ext.login import login_required

from ..extensions import db
from ..decorators import admin_required

from ..user import User, UserDetail
from .forms import UserForm, DeleteUserForm, CreateUserForm, SearchUserForm, DeleteProjectForm, CreateProjectForm, SearchProjectForm, ProjectForm

from ..project import Project


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('admin/index.html', users=users, active='index')


@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='users')

@admin.route('/createUser', methods=['GET', 'POST'])
@login_required
@admin_required
def createUser():
    form = CreateUserForm(next=request.args.get('next'))
    if form.validate_on_submit():
        user = User()
        user.user_detail = UserDetail()
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()
        flash('Usuario creado.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/createUser.html', form=form)

@admin.route('/searchUser', methods=['GET', 'POST'])
@login_required
@admin_required
def searchUser():
    form = SearchUserForm(next=request.args.get('next'))
    if form.validate_on_submit():
        user = User()
        user.user_detail = UserDetail()
        form.populate_obj(user)

        flash('Usuario encontrado.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/searchUser.html', form=form)
    
@admin.route('/user/<user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        flash('Usuario actualizado.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user.html', user=user, form=form)
    
@admin.route('/deleteUser/<user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def deleteUser(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = DeleteUserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.delete(user)
        db.session.commit()

        flash('Usuario eliminado.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/deleteUser.html', user=user, form=form)

@admin.route('/projects')
@login_required
@admin_required
def projects():
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects, active='projects')


@admin.route('/createProject', methods=['GET', 'POST'])
@login_required
@admin_required
def createProject():
    form = CreateProjectForm(next=request.args.get('next'))
    if form.validate_on_submit():
        project = Project()
        form.populate_obj(project)

        db.session.add(project)
        db.session.commit()
        flash('Proyecto creado.', 'success')
        return redirect(url_for('admin.projects'))

    return render_template('admin/createProject.html', form=form)


@admin.route('/searchProject', methods=['GET', 'POST'])
@login_required
@admin_required
def searchProject():
    form = SearchProjectForm(next=request.args.get('next'))
    if form.validate_on_submit():
        project = Project()
        form.populate_obj(project)

        flash('Proyecto encontrado.', 'success')
        return redirect(url_for('admin.projects'))

    return render_template('admin/searchProject.html', form=form)


@admin.route('/project/<project_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def project(project_id):
    project = Project.query.filter_by(id_proyecto=project_id).first_or_404()
    form = ProjectForm(obj=project, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(project)

        db.session.add(project)
        db.session.commit()

        flash('Proyecto actualizado.', 'success')
        return redirect(url_for('admin.projects'))

    return render_template('admin/project.html', project=project, form=form)



@admin.route('/deleteProject/<project_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def deleteProject(project_id):
    project = Project.query.filter_by(id_proyecto=project_id).first_or_404()
    form = DeleteProjectForm(obj=project, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(project)

        db.session.delete(project)
        db.session.commit()

        flash('Proyecto eliminado.', 'success')
        return redirect(url_for('admin.projects'))

    return render_template('admin/deleteProject.html', project=project, form=form)

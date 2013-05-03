# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required

from ..extensions import db
from ..decorators import admin_required

from ..modelos import User, Rol, Permiso, Proyecto, Comite
from .forms_adm import UserForm, DeleteUserForm, CreateUserForm
from .forms_adm import ComiteForm, BorrarComiteForm, CrearComiteForm
from .forms_adm import ProyectoForm, BorrarProyectoForm, CrearProyectoForm
from .forms_adm import RolForm, CrearRolForm , BorrarRolForm 
from .forms_adm import PermisoxRolForm, RolxUsuarioForm, UserxComiteForm

admin = Blueprint('admin', __name__, url_prefix='/admin')

#LOGIN

@admin.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('admin/index.html', users=users, active='index')
    
#USER

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
    roles = Rol.query.all()
    RolesAsignar = [item for item in roles]
    form = CreateUserForm(next=request.args.get('next'))
    form.rolPorUsuario.choices = [(h.id, h.nombre) for h in RolesAsignar ]
    if form.validate_on_submit():
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.password = form.password.data
        
        listaTotal=form.rolPorUsuario.data
        for rolID in listaTotal:
            rol = Rol.query.filter_by(id=rolID).first()
            user.rolPorUsuario = [rol]

        db.session.add(user)
        db.session.commit()
        flash('Usuario creado.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/createUser.html', form=form)

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

@admin.route('/searchUser')
def searchUser():
    keywords = request.args.get('keywords', '').strip()
    pagination=None   
       
    if keywords:
        page = int(request.args.get('page', 1))
        pagination= User.search(keywords).paginate(page,1)
    else:
        flash('Por favor, ingrese dato a buscar','error')
    return render_template('index/searchUser.html', pagination=pagination , keywords=keywords)

@admin.route('/')
#PERMISO
@admin.route('/permisos')
@login_required
@admin_required
def permisos():
    permisos = Permiso.query.all()
    return render_template('admin/permisos.html', permisos=permisos)
   
#ROL
@admin.route('/roles')
@login_required
@admin_required
def roles():
    roles = Rol.query.all()
    return render_template('admin/roles.html', roles=roles)

@admin.route('/crearRol', methods=['GET', 'POST'])
@login_required
@admin_required
def crearRol():
    permisos = Permiso.query.all()
    PermisosAsignar = [item for item in permisos]
    form = CrearRolForm(next=request.args.get('next')) 
    form.permisoPorRol.choices = [(h.id, h.nombre) for h in PermisosAsignar ]
       
    if form.validate_on_submit(): 
        rol = Rol()
        rol.nombre = form.nombre.data
        rol.descripcion = form.descripcion.data
             
        listaTotal=form.permisoPorRol.data
        for permisoID in listaTotal:
            permiso = Permiso.query.filter_by(id=permisoID).first()
            rol.permisoPorRol = [permiso]
            
        db.session.add(rol)
        db.session.commit()
       
        flash('Rol creado.', 'success')
        return redirect(url_for('admin.roles'))
       
    return render_template('admin/crearRol.html', form=form)

@admin.route('/rol/<rol_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def rol(rol_id):
    rol = Rol.query.filter_by(id=rol_id).first_or_404()
    form = RolForm(obj=rol, next = request.args.get('next'))
    roles = Rol.query.all()
            
    if form.validate_on_submit():
        for rolesTotales in roles:
            if form.nombre.data == rolesTotales.nombre and form.nombre.data <> rol.nombre :
                flash('El nombre del Rol ya existe', 'error')
                return redirect(url_for('admin.roles'))
            
        form.populate_obj(rol)    
        db.session.add(rol)
        db.session.commit()
        flash('Rol actualizado.', 'success')
        return redirect(url_for('admin.roles'))
    return render_template('admin/rol.html', rol=rol, form=form)


@admin.route('/borrarRol/<rol_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def borrarRol(rol_id):
    rol = Rol.query.filter_by(id=rol_id).first_or_404()
    form = BorrarRolForm(obj=rol, next=request.args.get('next'))
    users = rol.users.all()
    sum = 0
    for user in users:
        sum = sum + 1
    if sum <> 0:
        flash('Rol no eliminado. Rol asignado a usuario(s)', 'error')
        return redirect(url_for('admin.roles'))
    elif form.validate_on_submit():
        db.session.delete(rol)
        db.session.commit()
   
        flash('Rol eliminado.', 'success')
        return redirect(url_for('admin.roles'))

    return render_template('admin/borrarRol.html', rol=rol, form=form)

@admin.route('/searchRol')
def searchRol():
    keywords = request.args.get('keywords', '').strip()
    pagination=None   
       
    if keywords:
        page = int(request.args.get('page', 1))
        pagination= Rol.search(keywords).paginate(page,1)
    else:
        flash('Por favor, ingrese dato a buscar','error')
    return render_template('index/searchRol.html', pagination=pagination , keywords=keywords)

#PROYECTO
@admin.route('/proyectos')
@login_required
@admin_required
def proyectos():
    proyectos = Proyecto.query.all()
    return render_template('admin/proyectos.html', proyectos=proyectos, active='proyectos')

@admin.route('/crearProyecto', methods=['GET', 'POST'])
@login_required
@admin_required
def crearProyecto():
    form = CrearProyectoForm(next=request.args.get('next'))
    form.lider_proyecto.choices=[(g.id, g.nombre) for g in User.query.all()]
    
    if form.validate_on_submit():
        proyecto = Proyecto()
        form.populate_obj(proyecto)

        db.session.add(proyecto)
        db.session.commit()
        
        flash('Proyecto creado.', 'success')
        return redirect(url_for('admin.proyectos'))

    return render_template('admin/crearProyecto.html', form=form)

@admin.route('/buscarProyecto')
@login_required
@admin_required
def buscarProyecto():
    keywords = request.args.get('keywords', '').strip()
    pagination=None   
       
    if keywords:
        page = int(request.args.get('page', 1))
        pagination= Proyecto.search(keywords).paginate(page,1)
    else:
        flash('Por favor, ingrese dato a buscar','error')
    return render_template('index/buscarProyecto.html', pagination=pagination , keywords=keywords)


@admin.route('/proyecto/<proyecto_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def proyecto(proyecto_id):
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    form = ProyectoForm(obj=proyecto, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(proyecto)

        db.session.add(proyecto)
        db.session.commit()

        flash('Proyecto actualizado.', 'success')
        return redirect(url_for('admin.proyectos'))

    return render_template('admin/proyecto.html', proyecto=proyecto, form=form)

@admin.route('/borrarProyecto/<proyecto_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def borrarProyecto(proyecto_id):
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    form = BorrarProyectoForm(obj=proyecto, next=request.args.get('next'))
    
    if proyecto.comite is not None:
        flash('Proyecto no eliminado. Tiene asignado un comite', 'error')
        return redirect(url_for('admin.proyectos'))
    elif proyecto.estado_id is 1:
        flash('Proyecto no eliminado. Estado iniciado', 'error')
        return redirect(url_for('admin.proyectos'))
    else:
        if form.validate_on_submit():
            form.populate_obj(proyecto)
            db.session.delete(proyecto)
            db.session.commit()
    
            flash('Proyecto eliminado.', 'success')
            return redirect(url_for('admin.proyectos'))
        return render_template('admin/borrarProyecto.html', proyecto=proyecto, form=form)

#COMITE
@admin.route('/comites')
@login_required
@admin_required
def comites():
    comites = Comite.query.all()
    return render_template('admin/comites.html', comites=comites, active='comites')

@admin.route('/crearComite', methods=['GET', 'POST'])
@login_required
@admin_required
def crearComite():
    proyectos = Proyecto.query.filter_by(comite=None)
    form = CrearComiteForm(next=request.args.get('next'))
    form.proyecto_id.choices = [(h.id, h.nombre) for h in proyectos ]
       
    if form.validate_on_submit():      
        comite = Comite()
        form.populate_obj(comite)

        db.session.add(comite)
        db.session.commit()
        
        flash('Comite creado.', 'success')
        return redirect(url_for('admin.comites'))
       
    return render_template('admin/crearComite.html', form=form)

@admin.route('/buscarComite')
@login_required
@admin_required
def buscarComite():
    keywords = request.args.get('keywords', '').strip()
    pagination=None   
       
    if keywords:
        page = int(request.args.get('page', 1))
        pagination= Comite.search(keywords).paginate(page,1)
    else:
        flash('Por favor, ingrese dato a buscar','error')
    return render_template('index/buscarComite.html', pagination=pagination , keywords=keywords)



@admin.route('/comite/<comite_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def comite(comite_id):
    comite = Comite.query.filter_by(id=comite_id).first_or_404()
    form = ComiteForm(obj=comite, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(comite)

        db.session.add(comite)
        db.session.commit()

        flash('Comite actualizado.', 'success')
        return redirect(url_for('admin.comites'))

    return render_template('admin/comite.html', comite=comite, form=form)


@admin.route('/borrarComite/<comite_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def borrarComite(comite_id):
    comite = Comite.query.filter_by(id=comite_id).first_or_404()
    form = BorrarComiteForm(obj=comite, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(comite)

        db.session.delete(comite)
        db.session.commit()

        flash('Comite eliminado.', 'success')
        return redirect(url_for('admin.comites'))

    return render_template('admin/borrarComite.html', comite=comite, form=form)


#PROYECTO Miembro
@admin.route('/miembrosProyecto')
@login_required
@admin_required
def Miembros():
    users = User.query.all()
    return render_template('admin/proyectoMiembro.html', users=users, active='Miembros')

#PROYECTO Roles

@admin.route('/rolesProyecto')
@login_required
@admin_required
def Roles():
    roles = Rol.query.all()
    return render_template('admin/proyectoRol.html', roles=roles, active='Roles')


# RELACIONES

#Debe ser parecido a Roles en Admin Users

@admin.route('/usuariosxcomite/<comite_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def usuariosxcomite(comite_id):
    
    comite = Comite.query.filter_by(id=comite_id).first_or_404()
    form = UserxComiteForm(obj=comite, next=request.args.get('next'))
    usuariosAsignados = comite.usuarioPorComite
    todosUsuarios = User.query.all()
    UsuariosAsignar = [item for item in todosUsuarios if item not in usuariosAsignados]
    listaUsers = []
    for userAsig in usuariosAsignados:
        listaUsers.append(userAsig.id)
    
    form.usuarioPorComite.choices = [(h.id, h.name) for h in UsuariosAsignar ]
    
    if form.validate_on_submit():       
        listaTotal = form.usuarioPorComite.data
        for userAsig in listaUsers:
            listaTotal.append(userAsig)
        for userID in listaTotal:
            user = User.query.filter_by(id=userID).first()
            comite.usuarioPorComite = [user]            
            
        db.session.add(comite)
        db.session.commit()
       
        flash('Comite modificado.', 'success')
        return redirect(url_for('admin.comites'))
    
    return render_template('admin/usuariosxcomite.html', comite=comite, form=form, users=usuariosAsignados)  

    
@admin.route('/permisosxrol/<rol_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def permisosxrol(rol_id):

    rol = Rol.query.filter_by(id=rol_id).first_or_404()
    form = PermisoxRolForm(obj=rol, next=request.args.get('next'))
    permisosAsignados=rol.permisoPorRol
    todosPermisos=Permiso.query.all()
    PermisosAsignar= [item for item in todosPermisos if item not in permisosAsignados]
    listaPermisos=[]
    for permisoAsig in permisosAsignados:
        listaPermisos.append(permisoAsig.id)
       
    form.permisoPorRol.choices = [(h.id, h.nombre) for h in PermisosAsignar ]
       
    if form.validate_on_submit():       
        listaTotal=form.permisoPorRol.data
        for permisoAsig in listaPermisos:
            listaTotal.append(permisoAsig)
        for permisoID in listaTotal:
            permiso = Permiso.query.filter_by(id=permisoID).first()
            rol.permisoPorRol = [permiso]
        db.session.add(rol)
        db.session.commit()
       
        flash('Rol modificado.', 'success')
        return redirect(url_for('admin.roles'))
       
    return render_template('admin/permisosxrol.html', rol=rol, form=form, permisos=permisosAsignados)


@admin.route('/rolesxusuario/<user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def rolesxusuario(user_id):

    user = User.query.filter_by(id=user_id).first_or_404()
    form = RolxUsuarioForm(obj=user, next=request.args.get('next'))
    rolesAsignados = user.rolPorUsuario
    todosRoles = Rol.query.all()
    RolesAsignar = [item for item in todosRoles if item not in rolesAsignados]
    listaRoles=[]
    for rolAsig in rolesAsignados:
        listaRoles.append(rolAsig.id)
       
    form.rolPorUsuario.choices = [(h.id, h.nombre) for h in RolesAsignar ]
   
    if form.validate_on_submit():       
        listaTotal=form.rolPorUsuario.data
        for rolAsig in listaRoles:
            listaTotal.append(rolAsig)
        for rolID in listaTotal:
            rol = Rol.query.filter_by(id=rolID).first()
            user.rolPorUsuario = [rol]
        db.session.add(user)
        db.session.commit()
       
        flash('Usuario modificado.', 'success')
        return redirect(url_for('admin.users'))
       
    return render_template('admin/rolesxusuario.html', user=user, form=form, roles=rolesAsignados)

#@admin.route('/usuarioxproyecto/<proyecto_id>', methods=['GET', 'POST'])
#@login_required
#@admin_required
#def usuarioxproyecto(proyecto_id):
#    
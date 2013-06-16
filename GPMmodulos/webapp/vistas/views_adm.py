# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user

from ..extensions import db
from ..decorators import *



#from ..modelos import User, Rol, Permiso, Proyecto, Comite, Fase, HistorialItem

from ..modelos import *
from .forms_adm import *
#from .forms_adm import UserForm, DeleteUserForm, CreateUserForm
#from .forms_adm import ComiteForm, BorrarComiteForm, CrearComiteForm
#from .forms_adm import ProyectoForm, BorrarProyectoForm, CrearProyectoForm
#from .forms_adm import RolForm, CrearRolForm , BorrarRolForm 
#from .forms_adm import PermisoxRolForm, RolxUsuarioForm, UserxComiteForm, UsuarioxProyectoForm, RolxProyectoForm
#from .forms_adm import CrearFaseForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


#USER

@admin.route('/')
@login_required
def index():
    users = User.query.all()
    return render_template('admin/index.html', users=users, active='index')
    
@admin.route('/users')
@login_required
def users():
    """Funcion que lista los usuarios del sistema"""
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='users')

@admin.route('/createUser', methods=['GET', 'POST'])
@login_required
@crearUsuarios_required
def createUser():
    """Funcion encargada de crear Usuario asignando un rol o mas."""
    roles = Rol.query.all()
    RolesAsignar = [item for item in roles]
    form = CreateUserForm(next=request.args.get('next'))
    form.rolPorUsuario.choices = [(h.id, h.nombre) for h in RolesAsignar ]
    if form.validate_on_submit():
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.password = form.password.data
        
        listaTotal = form.rolPorUsuario.data
        for rolID in listaTotal:
            rol = Rol.query.filter_by(id=rolID).first()
            user.rolPorUsuario.append(rol)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Usuario creado.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/createUser.html', form=form)

@admin.route('/user/<user_id>', methods=['GET', 'POST'])
@login_required
@login_required
@modificarUsuarios_required
def user(user_id):
    """Funcion encargada de Editar un usuario"""
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
@eliminarUsuarios_required
def deleteUser(user_id):
    """Funcion encargada de eliminar un usuario del sistema"""
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
@login_required
@verUsuarios_required
def searchUser():
    """Funcion encargada de la busqueda de un usuario por nombre o email"""
    keywords = request.args.get('keywords', '').strip()
    pagination=None   
       
    if keywords:
        page = int(request.args.get('page', 1))
        pagination= User.search(keywords).paginate(page,1)
    else:
        flash('Por favor, ingrese dato a buscar','error')
    return render_template('index/searchUser.html', pagination=pagination , keywords=keywords)

#PERMISO

@admin.route('/permisos')
@login_required
@verPermisos_required
def permisos():
    """Funcion que lista los permisos del sistema"""
    permisos = Permiso.query.all()
    return render_template('admin/permisos.html', permisos=permisos)

@admin.route('/permisosxrol/Rol<rol_id>/Permiso<permiso_id>', methods=['GET', 'POST'])
@login_required
#@desasignarPermiso_required
def desasignarPermiso(rol_id, permiso_id):
    """Funcion que permite desasignar un permiso"""    
    permisoDesasignar = Permiso.query.filter_by(id=permiso_id).first_or_404()
    rol = Rol.query.filter_by(id=rol_id).first_or_404()
    form = PermisoxRolForm(obj=user, next=request.args.get('next'))
    permisosAsignados = rol.permisoPorRol
    
    for item in permisosAsignados:
        if item == permisoDesasignar:
            rol.permisoPorRol.remove(item)
            db.session.add(rol)
            db.session.commit()
            flash('Permiso desasignado.', 'success')
            return redirect(url_for('admin.permisosxrol', rol_id=rol.id))
     
    return render_template('admin/permisosxrol.html', rol=rol, form=form, permisos=permisosAsignados)

#ROL

@admin.route('/roles')
@login_required
@verRoles_required
def roles():
    """Funcion que lista los roles del sistema"""
    roles = Rol.query.all()
    return render_template('admin/roles.html', roles=roles)

@admin.route('/crearRol', methods=['GET', 'POST'])
@login_required
@crearRoles_required
def crearRol():
    """Funcion que permite crear un rol en el sistema asignando uno o mas permisos"""
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

            #rol.permisoPorRol = [permiso]
            rol.permisoPorRol.append(permiso)
            
        db.session.add(rol)
        db.session.commit()
       
        flash('Rol creado.', 'success')
        return redirect(url_for('admin.roles'))
       
    return render_template('admin/crearRol.html', form=form)

@admin.route('/rol/<rol_id>', methods=['GET', 'POST'])
@login_required
@modificarRoles_required
def rol(rol_id):
    """Funcion que permite editar un rol"""
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



@admin.route('/borrarRol/<proyecto_id>/<rol_id>', methods=['GET', 'POST'])
@login_required
#@eliminarRoles_required
def borrarRol (proyecto_id, rol_id):
    """Funcion que permite eliminar un rol de un proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    rol = Rol.query.filter_by(id=rol_id).first_or_404()
    
    if (rol.tieneUsuarios(proyecto.usuarioPorProyecto)):
        flash('No se puede eliminar el Rol porque esta asignado a otros usuarios dentro del Proyecto', 'error')
        return redirect(url_for('admin.rolesxproyecto', proyecto_id=proyecto.id))
        
    proyecto.roles.remove(rol)
    db.session.add(proyecto)
    db.session.commit()
    
    flash('Rol eliminado.', 'success')
    return redirect(url_for('admin.rolesxproyecto', proyecto_id=proyecto.id))
      
    
    


@admin.route('/rolesxusuario/User<user_id>/Rol<rol_id>', methods=['GET', 'POST'])
@login_required
#@desasignarRol_required
def desasignarRol(user_id, rol_id):
    """Funcion que permite desasignar un rol"""
    rolDesasignar = Rol.query.filter_by(id=rol_id).first_or_404()
    user = User.query.filter_by(id=user_id).first_or_404()
    form = RolxUsuarioForm(obj=user, next=request.args.get('next'))
    rolesAsignados = user.rolPorUsuario
    
    for item in rolesAsignados:
        if item == rolDesasignar:
            user.rolPorUsuario.remove(item)
            db.session.add(user)
            db.session.commit()
            flash('Rol desasignado.', 'success')
            return redirect(url_for('admin.rolesxusuario', user_id=user.id))
     
    return render_template('admin/rolesxusuario.html', user=user, form=form, roles=rolesAsignados)

@admin.route('/searchRol')
#@verRoles_required
def searchRol():
    """Funcion que realiza una busqueda de roles por nombre"""
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
#@verProyectos_required
def proyectos():
    """Funcion que lista los proyectos del sistema"""
    proyectos = Proyecto.query.all()
    return render_template('admin/proyectos.html', proyectos=proyectos, active='proyectos')

@admin.route('/crearProyecto', methods=['GET', 'POST'])
@login_required
#@crearProyectos_required
def crearProyecto():
    """Funcion que permite la creacion de un Proyecto"""
    form = CrearProyectoForm(next=request.args.get('next'))
    form.lider_proyecto.choices=[(g.id, g.nombre) for g in User.query.all()]
    
    if form.validate_on_submit():
        proyecto = Proyecto()
        user = User.query.filter_by(id=form.lider_proyecto.data).first_or_404()
        proyecto.usuarioPorProyecto = [user]
        proyecto.nombre = form.nombre.data
        proyecto.numero_fases = form.numero_fases.data
        proyecto.lider_proyecto = form.lider_proyecto.data
        proyecto.descripcion = form.descripcion.data
#        form.populate_obj(proyecto)

        db.session.add(proyecto)
        db.session.commit()
        
        flash('Proyecto creado.', 'success')
        return redirect(url_for('admin.proyectos'))

    return render_template('admin/crearProyecto.html', form=form)

@admin.route('/buscarProyecto')
@login_required
@eliminarProyectos_required
def buscarProyecto():
    """Funcion que filtra los proyectos por nombre"""
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
@modificarProyectos_required
def proyecto(proyecto_id):
    """Funcion que permite editar un Proyecto"""
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
@eliminarProyectos_required
def borrarProyecto(proyecto_id):
    """Funcion que permite eliminar un Proyecto del sistema"""
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
 
@admin.route('/usuarioxproyecto/Proyecto<proyecto_id>/Usuario<user_id>', methods=['GET', 'POST'])
@login_required
#@desasignarUsuario_required
def desasignarUsuario(proyecto_id, user_id):
    """Funcion que permite desasignar a un usuario de un proyecto"""
    usuarioDesasignar = User.query.filter_by(id=user_id).first_or_404()
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    form = UsuarioxProyectoForm(obj=user, next=request.args.get('next'))
    usuariosAsignados = proyecto.usuarioPorProyecto
      
    for item in usuariosAsignados:
        if item == usuarioDesasignar:
            proyecto.usuarioPorProyecto.remove(item)
            #desasignarMiembro(proyecto.comite.id, usuarioDesasignar.id)
            db.session.add(proyecto)
            db.session.commit()
            flash('Usuario desasignado.', 'success')
            return redirect(url_for('admin.usuariosxproyecto', proyecto_id=proyecto.id))
       
    return render_template('admin/usuariosxproyecto.html', proyecto=proyecto, form=form, users=usuariosAsignados)


#COMITE

#@admin.route('/comites')
#@login_required
#@verComites_required
#def comites():
#    """Funcion que lista los comites existentes en el sistema"""
#    comites = Comite.query.all()
#    return render_template('admin/comites.html', comites=comites, active='comites')
#
#@admin.route('/crearComite', methods=['GET', 'POST'])
#@login_required
#@crearComites_required
#def crearComite():
#    """Funcion que permite la creacion de un comite"""
#    proyectos = Proyecto.query.filter_by(comite=None)
#    form = CrearComiteForm(next=request.args.get('next'))
#    form.proyecto_id.choices = [(h.id, h.nombre) for h in proyectos ]
#       
#    if form.validate_on_submit():      
#        comite = Comite()
#        proyecto = Proyecto.query.filter_by(id=form.proyecto_id.data).first_or_404()
#        lider = proyecto.lider_proyecto
#        user = User.query.filter_by(id=lider).first_or_404()
#        comite.proyecto_id = proyecto.id
#        comite.usuarioPorComite = [user]
#        comite.nombre = form.nombre.data
#        comite.descripcion = form.descripcion.data
#
#        db.session.add(comite)
#        db.session.commit()
#        
#        flash('Comite creado.', 'success')
#        return redirect(url_for('admin.comites'))
#       
#    return render_template('admin/crearComite.html', form=form)
#
#@admin.route('/buscarComite')
#@login_required
#@verComites_required
#def buscarComite():
#    """FUncion que busca un comite por nombre"""
#    keywords = request.args.get('keywords', '').strip()
#    pagination=None   
#       
#    if keywords:
#        page = int(request.args.get('page', 1))
#        pagination= Comite.search(keywords).paginate(page,1)
#    else:
#        flash('Por favor, ingrese dato a buscar','error')
#    return render_template('index/buscarComite.html', pagination=pagination , keywords=keywords)
#
#@admin.route('/comite/<comite_id>', methods=['GET', 'POST'])
#@login_required
#@modificarComites_required
#def comite(comite_id):
#    """Funcion que permite editar un comite"""
#    comite = Comite.query.filter_by(id=comite_id).first_or_404()
#    form = ComiteForm(obj=comite, next=request.args.get('next'))
#
#    if form.validate_on_submit():
#        form.populate_obj(comite)
#
#        db.session.add(comite)
#        db.session.commit()
#
#        flash('Comite actualizado.', 'success')
#        return redirect(url_for('admin.comites'))
#
#    return render_template('admin/comite.html', comite=comite, form=form)
#
#@admin.route('/borrarComite/<comite_id>', methods=['GET', 'POST'])
#@login_required
#@eliminarComites_required
#def borrarComite(comite_id):
#    """Funcion que permite la eliminacion de un comite"""
#    comite = Comite.query.filter_by(id=comite_id).first_or_404()
#    form = BorrarComiteForm(obj=comite, next=request.args.get('next'))
#
#    if form.validate_on_submit():
#        form.populate_obj(comite)
#
#        db.session.delete(comite)
#        db.session.commit()
#
#        flash('Comite eliminado.', 'success')
#        return redirect(url_for('admin.comites'))
#
#    return render_template('admin/borrarComite.html', comite=comite, form=form)
#
#@admin.route('/usuariosxcomite/Comite<comite_id>/Usuario<user_id>', methods=['GET', 'POST'])
#@login_required
##@desasignarMiembro_required
#def desasignarMiembro(comite_id, user_id):
#    """Funcion que permite desasignar a un usuario de un comite"""
#    miembroDesasignar = User.query.filter_by(id=user_id).first_or_404()
#    comite = Comite.query.filter_by(id=comite_id).first_or_404()
#    form = UserxComiteForm(obj=user, next=request.args.get('next'))
#    miembrosAsignados = comite.usuarioPorComite
#    
#    for item in miembrosAsignados:
#        if item == miembroDesasignar:
#            comite.usuarioPorComite.remove(item)
#            db.session.add(comite)
#            db.session.commit()
#            flash('Miembro desasignado.', 'success')
#            return redirect(url_for('admin.usuariosxcomite', comite_id=comite.id))
#    
#    return render_template('admin/usuariosxcomite.html', comite=comite, form=form, users=miembrosAsignados)

#FASES

@admin.route('/crearFase/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def crearFase(proyecto_id):
    """Funcion que permite instanciar una Fase de un Proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    if proyecto.fases.count() < proyecto.numero_fases:
        form = CrearFaseForm(next=request.args.get('next'))
        if form.validate_on_submit():
            fase = Fase()
            fase.nombre = form.nombre.data
            fase.descripcion = form.descripcion.data
            fase.proyecto_id = proyecto.id
            
            db.session.add(fase)
            db.session.commit()
            
            flash('Fase creada.', 'success')
            return redirect(url_for('admin.fasesxproyecto',proyecto_id=proyecto.id))
            
        return render_template('admin/crearFase.html', proyecto=proyecto, form=form)
    else:
        flash('Numero de fases del proyecto alcanzado', 'error')
        return redirect(url_for('admin.fasesxproyecto',proyecto_id=proyecto.id))

@admin.route('/IdF<fase_id>/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def fase(proyecto_id, fase_id):
    """Funcion que permite editar un comite"""
    fase = Fase.query.filter_by(id=fase_id).first_or_404()
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    form = FaseForm(obj=fase, next=request.args.get('next'))
    if form.validate_on_submit():
        form.populate_obj(fase)

        db.session.add(fase)
        db.session.commit()

        flash('Fase actualizada.', 'success')
        return redirect(url_for('admin.fasesxproyecto',proyecto_id=proyecto.id))

    return render_template('admin/fase.html', fase=fase, proyecto=proyecto, form=form)

# TIPO DE ITEM

@admin.route('/crearTipoItem/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def crearTipoItem(proyecto_id):
    """Funcion que permite crear un Tipo de Item en un Proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    form = CrearTipoItemForm(next=request.args.get('next'))

    if form.validate_on_submit():
        tipoItem = TipoItem()
        tipoItem.nombre = form.nombre.data
        tipoItem.descripcion = form.descripcion.data
        tipoItem.proyecto_id = proyecto.id
            
        db.session.add(tipoItem)
        db.session.commit()
            
        flash('Tipo de Item creado.', 'success')
        return redirect(url_for('admin.tiposItemxproyecto',proyecto_id=proyecto.id))
            
    return render_template('admin/crearTipoItem.html', proyecto=proyecto, form=form)


@admin.route('/crearAtributo/<proyecto_id>/<tipoItem_id>', methods=['GET', 'POST'])
@login_required
def crearAtributo(proyecto_id, tipoItem_id):
    """Funcion que permite crear Atributo a tipo de item"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    tipoItem = TipoItem.query.filter_by(id=tipoItem_id).first_or_404()
    
    atributos = Atributo.query.all()
    form = CrearAtributoForm(next=request.args.get('next'))
    form.atributo_id.choices=[(h.id, h.nombre) for h in atributos]
   
    if form.validate_on_submit():
        atributo = Atributo()
        atributo.nombre = form.nombre.data
        atributo.valorString = form.valor.data
                
        db.session.add(atributo)
        db.session.commit()
        
        
#        tipoItem.atributoPorTipoItem = atributo.id          
#        
#        db.session.add(tipoItem)
#        db.session.commit()
#            
        flash('Atributo agregado.', 'success')
        return redirect(url_for('admin.tiposItemxproyecto',proyecto_id=proyecto.id))
            
    return render_template('admin/crearAtributo.html', proyecto=proyecto, tipoItem=tipoItem, form=form)


@admin.route('/TI<tipoItem_id>/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def tipoItem(proyecto_id, tipoItem_id):
    """Funcion que permite editar un comite"""
    tipoItem = TipoItem.query.filter_by(id=tipoItem_id).first_or_404()
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    form = TipoItemForm(obj=tipoItem, next=request.args.get('next'))
    if form.validate_on_submit():
        form.populate_obj(tipoItem)

        db.session.add(tipoItem)
        db.session.commit()

        flash('Tipo de Item actualizada.', 'success')
        return redirect(url_for('admin.tiposItemxproyecto',proyecto_id=proyecto.id))

    return render_template('admin/tipoItem.html', tipoItem=tipoItem, proyecto=proyecto, form=form)

@admin.route('/<proyecto_id>/<tipoItem_id>', methods=['GET', 'POST'])
@login_required
def importarTipoItem(proyecto_id, tipoItem_id):
    """Funcion que permite editar un comite"""
    proyecto = Proyecto.query.filter_by(id = proyecto_id).first_or_404()
    tipoItem = TipoItem.query.filter_by(id=tipoItem_id).first_or_404()
    
    nuevotipoItem = TipoItem()
    nuevotipoItem.nombre = tipoItem.nombre
    nuevotipoItem.descripcion = tipoItem.descripcion
    nuevotipoItem.atributo = tipoItem.atributoPorTipoItem
    nuevotipoItem.proyecto_id = proyecto.id
        
    db.session.add(nuevotipoItem)
    db.session.commit()

    flash('Tipo de Item importado correctamente..', 'success')
    return redirect(url_for('admin.tiposItemxproyecto',proyecto_id=proyecto.id))
    



@admin.route('/buscarTipoItem')
@login_required
@admin_required
def buscarTipoItem():
    """FUncion que busca un Tipo de Item por nombre"""
    keywords = request.args.get('keywords', '').strip()
    pagination=None   
       
    if keywords:
        page = int(request.args.get('page', 1))
        pagination= TipoItem.search(keywords).paginate(page,1)
    else:
        flash('Por favor, ingrese dato a buscar','error')
    return render_template('index/buscarTipoItem.html', pagination=pagination , keywords=keywords)

##########################################################################        
# RELACIONES

#@admin.route('/usuariosxcomite/<comite_id>', methods=['GET', 'POST'])
#@login_required
#@verMiembrosComites_required
#def usuariosxcomite(comite_id):
#    """Funcion que asigna los usuarios de un proyecto a un comite"""
#    comite = Comite.query.filter_by(id=comite_id).first_or_404()
#    proyecto = Proyecto.query.filter_by(id=comite.proyecto_id).first_or_404()
#    form = UserxComiteForm(obj=comite, next=request.args.get('next'))
#    usuariosAsignados = comite.usuarioPorComite
#    todosUsuarios = proyecto.usuarioPorProyecto
##    todosUsuarios = User.query.all()
#    UsuariosAsignar = [item for item in todosUsuarios if item not in usuariosAsignados]
#    listaUsers = []
#    for userAsig in usuariosAsignados:
#        listaUsers.append(userAsig.id)
#    
#    form.usuarioPorComite.choices = [(h.id, h.nombre) for h in UsuariosAsignar ]
#    
#    if form.validate_on_submit():       
#        listaTotal = form.usuarioPorComite.data
#        for userAsig in listaUsers:
#            listaTotal.append(userAsig)
#        for userID in listaTotal:
#            user = User.query.filter_by(id=userID).first()
#            comite.usuarioPorComite.append(user)            
#            
#        db.session.add(comite)
#        db.session.commit()
#       
#        flash('Miembro asignado.', 'success')
#        return redirect(url_for('admin.usuariosxcomite', comite_id=comite.id))
#    
#    return render_template('admin/usuariosxcomite.html', comite=comite, form=form, users=usuariosAsignados)  

@admin.route('/permisosxrol/<rol_id>', methods=['GET', 'POST'])
@login_required
@eliminarUsuarios_required
def permisosxrol(rol_id):
    """Funcion que asigna los permisos a un rol"""
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
            rol.permisoPorRol.append(permiso)
        db.session.add(rol)
        db.session.commit()
        
        if len(PermisosAsignar)==1:
            flash('Permiso asignado.', 'success')
        else:
            flash('Permisos asignados.', 'success')
        
        return redirect(url_for('admin.permisosxrol', rol_id=rol.id))
       
    return render_template('admin/permisosxrol.html', rol=rol, form=form, permisos=permisosAsignados)

@admin.route('/rolesxusuario/<user_id>', methods=['GET', 'POST'])
@login_required
@verUsuarios_required
def rolesxusuario(user_id):
    """Funcion que asigna los roles a un usuario"""
    user = User.query.filter_by(id=user_id).first_or_404()
    form = RolxUsuarioForm(obj=user, next=request.args.get('next'))
    rolesActuales = user.rolPorUsuario
    todosRoles = Rol.query.all()
    #RolesAsignar = [item for item in todosRoles if item not in rolesAsignados]
    
    rolesDisponibles=[]
    for item in todosRoles:
        if item not in rolesActuales:
            rolesDisponibles.append(item)
            print item.nombre
            print "*************Roles disponibles"
    
    
    listaRolesActuales=[]
    for rol in rolesActuales:
        print rol.nombre
        print "##################Roles actuales"
        #listaRolesActuales.append(rol.id) #carga en una listaroles el id de los roles actuales
        listaRolesActuales.append(rol)
       
    #form.rolPorUsuario.choices = [(h.id, h.nombre) for h in RolesAsignar ]
    #for h in rolesDisponibles:
        #form.rolPorUsuario.choices=(h.id)
    form.rolPorUsuario.choices = [(h.id, h.nombre) for h in rolesDisponibles ]
    
    if form.validate_on_submit():       

        listaRolesSeleccionados=form.rolPorUsuario.data  # trae el id de los roles que seleccion
        
        print listaRolesSeleccionados
        print "++++++++ roles seleccionados para agregar"
                    
        for rolAsig in listaRolesActuales:    # a la lista de roles que ya tiene, le agrega lo que selecciono
            listaRolesSeleccionados.append(rolAsig.id)
        
        print listaRolesSeleccionados
        print "++++++++ la lista una vez que vez que le agrego"
                     
        for rolID in listaRolesSeleccionados:
            role=Rol.query.filter_by(id=rolID).first_or_404()
            user.rolPorUsuario.append(role)
            
        #variable de prueba para imprimir nomas
        nuevosRoles = user.rolPorUsuario
        
        for nuevoRol in nuevosRoles:
            print nuevoRol.nombre
            print "####### Los nuevos roles y se commitea"    
        

        db.session.add(user)
        db.session.commit()
       
        flash('Usuario modificado.', 'success')
        return redirect(url_for('admin.users'))
       
    return render_template('admin/rolesxusuario.html', user=user, form=form, roles=listaRolesActuales)

####################################################################
#            PROYECTO CONFIGURACION

@admin.route('/usuarioxproyecto/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def usuariosxproyecto(proyecto_id):
    """Funcion que asigna los usuarios de un proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    form = UsuarioxProyectoForm(obj=proyecto, next=request.args.get('next'))
    usuariosActuales = proyecto.usuarioPorProyecto
    todosUsuarios = User.query.all()
    
    #UsersAsignar = [item for item in todosUsuarios if item not in usersAsignados]
    
    usuariosDisponibles=[]
    for item in todosUsuarios:
        if item not in usuariosActuales:
            usuariosDisponibles.append(item)
            print item.nombre
            print "*************Usuarios disponibles"
    
    listaUsuariosActuales=[]
    for usuario in usuariosActuales:
        print usuario.nombre
        print "##################Usuarios actuales del proyect0"
        listaUsuariosActuales.append(usuario)
       
    form.usuarioPorProyecto.choices = [(h.id, h.nombre) for h in usuariosDisponibles ]
    
    if form.validate_on_submit():       

        listaUsuariosSeleccionados=form.usuarioPorProyecto.data
        
        print listaUsuariosSeleccionados
        print "++++++++ usuarios seleccionados para agregar"
                    
        for userAsig in listaUsuariosActuales:    # a la lista de usuarios que ya tiene, le agrega lo que selecciono
            listaUsuariosSeleccionados.append(userAsig.id)
        
        print listaUsuariosSeleccionados
        print "++++++++ la lista una vez que vez que le agrego"
                     
        for userID in listaUsuariosSeleccionados:
            usere=User.query.filter_by(id=userID).first_or_404()
            proyecto.usuarioPorProyecto.append(usere)
            
        #variable de prueba para imprimir nomas
        nuevosUsuarios = proyecto.usuarioPorProyecto
        
        for nuevoUser in nuevosUsuarios:
            print nuevoUser.nombre
            print "####### Los nuevos Usuarios y se commitea"    
            
        db.session.add(proyecto)
        db.session.commit()
       
        flash('Usuario agregado al proyecto.', 'success')
        return redirect(url_for('admin.usuariosxproyecto', proyecto_id=proyecto.id))
       
    return render_template('admin/usuarioxproyecto.html', proyecto=proyecto, form=form, users=listaUsuariosActuales, active='Miembros')

@admin.route('/rolesxproyecto/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def rolesxproyecto(proyecto_id):
    """Funcion que asigna los roles de un proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    form = RolxProyectoForm(obj=proyecto, next=request.args.get('next'))
    rolesActuales = proyecto.roles
    todosRoles = Rol.query.all()
    rolesCandidatos = [item for item in todosRoles if item not in rolesActuales]
    listaRoles=[]
    for rolAct in rolesActuales:
        listaRoles.append(rolAct.id)
       
    form.roles.choices = [(m.id, m.nombre) for m in rolesCandidatos ]
   
    if form.validate_on_submit():       
        listaTotal=form.roles.data
        for rolAct in listaRoles:
            listaTotal.append(rolAct)
        for rolID in listaTotal:
            rol = Rol.query.filter_by(id=rolID).first()
            proyecto.roles.append(rol)
        db.session.add(proyecto)
        db.session.commit()
       
        flash('Proyecto modificado.', 'success')
        return redirect(url_for('admin.proyectos'))
       
    return render_template('admin/rolesxproyecto.html', proyecto=proyecto, form=form, roles=rolesActuales, active='Roles')

@admin.route('/fasesxproyecto/<proyecto_id>', methods=['GET', 'POST'])
@login_required

def fasesxproyecto(proyecto_id):
    """Funcion que lista las fases de un Proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    fasesExistentes = proyecto.fases
#   fases = Fase.query.filter_by(proyecto_id=proyecto.id).first_or_404
    return render_template('admin/fasesxproyecto.html', proyecto=proyecto, fases=fasesExistentes, active='Fases')

@admin.route('/tiposItemxproyecto/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def tiposItemxproyecto(proyecto_id):
    """Funcion que lista los tipos de Item de un Proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    tiposItemExistentes = proyecto.tiposItem
    return render_template('admin/tiposItemxproyecto.html', proyecto=proyecto, tiposItem=tiposItemExistentes, active='Tipos de Item')

#@admin.route('/historialxitem/<item_id>', methods=['GET', 'POST'])
#@login_required
#def historialxitem(item_id):
#    """Funcion que lista el historial de un Item"""
#    item = Item.query.filter_by(id=item_id).first_or_404()
#    todosHistoriales = HistorialItem.query.all()
#    
#    historiales=[]
#    for historial in todosHistoriales:
#        if historial.itemId==item.id:
#            historiales.append(historial)
#    return render_template('admin/historialxitem.html', item=item, historiales=historiales)
#    
#    
    
#
#@admin.route('/itemsxproyecto/<proyecto_id>', methods=['GET', 'POST'])
#@login_required
#def itemsxproyecto(proyecto_id):
#    """Funcion que lista las fases de un Proyecto"""
#    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
#    itemsExistentes = proyecto.items
##   fases = Fase.query.filter_by(proyecto_id=proyecto.id).first_or_404
#    return render_template('admin/itemsxproyecto.html', proyecto=proyecto, items=itemsExistentes, active='Items')
#
#
#@admin.route('/crearItem/<proyecto_id>', methods=['GET', 'POST'])
#@login_required
#def crearItem(proyecto_id):
#    """Funcion que permite instanciar un Item de un Proyecto"""
#    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
#    tiposItem= TipoItem.query.filter_by(proyecto_id=proyecto_id)
#    form = CrearItemForm(next=request.args.get('next'))
#    form.tipoItem_id.choices = [(h.id, h.nombre) for h in tiposItem ]
#    if form.validate_on_submit():
#        item = Item()
#        tipoItem = TipoItem.query.filter_by(id=form.tipoItem_id.data).first_or_404()
#        item.nombre = form.nombre.data
#        item.descripcion = form.descripcion.data
#        item.proyecto_id = proyecto.id
#        item.tipoItem_id = tipoItem.id
#        
#        db.session.add(item)
#        db.session.commit()
#        
#        historial = HistorialItem()
#        historial.itemId=item.id
#        historial.descripcion= current_user.nombre+" creo el item, con nombre: " + item.nombre
#        
#        db.session.add(historial)
#        db.session.commit()
#     
#        
#        flash('Item creado.', 'success')
#        return redirect(url_for('admin.itemsxproyecto',proyecto_id=proyecto.id))
#        
#    return render_template('admin/crearItem.html', proyecto=proyecto, form=form)
#
#
#@admin.route('/IdItem<item_id>/<proyecto_id>', methods=['GET', 'POST'])
#@login_required
#def item(proyecto_id, item_id):
#    """Funcion que permite editar un item"""
#    item = Item.query.filter_by(id=item_id).first_or_404()
#    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
#    form = ItemForm(obj=item, next=request.args.get('next'))
#    if form.validate_on_submit():
#        form.populate_obj(item)
#
#        db.session.add(item)
#        db.session.commit()
#
#        historial = HistorialItem()
#        historial.itemId=item.id
#        historial.descripcion= current_user.nombre+" modifico el item." 
#        
#        db.session.add(historial)
#        db.session.commit()
#     
#        flash('Item actualizado.', 'success')
#        return redirect(url_for('admin.itemsxproyecto',proyecto_id=proyecto.id))
#
#    return render_template('admin/item.html', item=item, proyecto=proyecto, form=form)

#
#@admin.route('/lineaBasexproyecto/<proyecto_id>', methods=['GET', 'POST'])
#@login_required
#def lineaBasexproyecto(proyecto_id):
#    """Funcion que lista las lineas base de un Proyecto"""
#    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
#    fases = proyecto.fases
#    
#    listaDeLB = []
#    for fase in fases:
#        faseElegida = Fase.query.filter_by(id=fase.id).first_or_404()
#        lb = faseElegida.lineaBase
#        for linea in lb:
#            lineaBase = LineaBase.query.filter_by(id=linea.id).first_or_404()
#            listaDeLB.append(lineaBase)
#    
#    return render_template('cambios/lineaBasexproyecto.html', proyecto=proyecto, fases=fases, lineasBases=listaDeLB, active='Lineas Base')
#
#@admin.route('/crearLineaBase/<proyecto_id>', methods=['GET', 'POST'])
#@login_required
#def crearLineaBase(proyecto_id):
#    """Funcion que permite instanciar una Linea Base de una Fase"""
#    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
#    fases = Fase.query.filter_by(proyecto_id=proyecto_id)
#    form = CrearLineaBaseForm(next=request.args.get('next'))
#    form.fase_id.choices = [(h.id, h.nombre) for h in fases ]
#    
#    if form.validate_on_submit():
#        lineabase = LineaBase()
#        fase = Fase.query.filter_by(id=form.fase_id.data).first_or_404()
#        lineabase.numero_lb = form.numero_lb.data
#        lineabase.descripcion = form.descripcion.data
#        lineabase.fase_id = fase.id
#        
#        db.session.add(lineabase)
#        db.session.commit()
#        
#        historial = HistorialLineaBase()
#        historial.lineaBase_id = lineabase.id
#        historial.descripcion= current_user.nombre+" creo la Linea Base " +str(lineabase.numero_lb)+ " de la Fase " +str(lineabase.fase_id)
#        
#        db.session.add(historial)
#        db.session.commit()
#        
#        flash('Linea Base creada.', 'success')
#        return redirect(url_for('admin.lineaBasexproyecto',proyecto_id=proyecto.id))
#    
#    return render_template('cambios/crearLineaBase.html', proyecto=proyecto, form=form)
#
#@admin.route('/historialxlineabase/<lineabase_id>', methods=['GET', 'POST'])
#@login_required
#def historialxlineabase(lineabase_id):
#    """Funcion que lista el historial de un Item"""
#    lineabase = LineaBase.query.filter_by(id=lineabase_id).first_or_404()
#    todosHistoriales = HistorialLineaBase.query.all()
#    
#    historiales=[]
#    for historial in todosHistoriales:
#        if historial.lineaBase_id==lineabase.id:
#            historiales.append(historial)
#    return render_template('cambios/historialxlineabase.html', lineabase=lineabase, historiales=historiales)
#
#@admin.route('/lineaBasexproyecto/<proyecto_id>/<lineabase_id>', methods=['GET', 'POST'])
#@login_required
##@modificarProyectos_required
#def lineaBase(proyecto_id, lineabase_id):
#    """Funcion que permite editar una Linea Base"""
#    lineaBase = LineaBase.query.filter_by(id=lineabase_id).first_or_404()
#    form = LineaBaseForm(obj=lineaBase, next=request.args.get('next'))
#    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
#    #fases = proyecto.fases
#
#    if form.validate_on_submit():
#        form.populate_obj(lineaBase)
#
#        db.session.add(lineaBase)
#        db.session.commit()
#
#        flash('Linea Base actualizado.', 'success')
#        return redirect(url_for('admin.lineaBasexproyecto', proyecto_id=proyecto.id, lineabase_id=lineaBase.id))
#
#    return render_template('cambios/lineaBase.html', proyecto=proyecto, lineabase=lineaBase, form=form)

#@admin.route('/IT<item_id>/PR<proyecto_id>', methods=['GET', 'POST'])
#@login_required
#def crearSolicitud(proyecto_id, item_id):
#    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
#    comite = proyecto.comite
#    item = Item.query.filter_by(id=item_id).first_or_404()
#    usuariosComite = comite.usuarioPorComite
#    itemsExistentes = proyecto.items
#    
#    solicitud = Solicitud()
#    solicitud.comite_id = comite.id
#    solicitud.item_id = item_id
#    db.session.add(solicitud)
#    db.session.commit()
#    
#    for usuario in usuariosComite:
#        usuario.solicitudPorUsuario.append(solicitud)
#        print '#################usuario'
#        print usuario.nombre
#        
#        db.session.add(usuario)
#        db.session.commit()
#    
#    flash('Solicitud enviada correctamente.', 'success')
#   
#    return render_template('admin/itemsxproyecto.html', proyecto=proyecto, items=itemsExistentes, active='Items')
#    
#    


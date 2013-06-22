from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user

from ..extensions import db
from ..decorators import crearUsuarios_required, modificarUsuarios_required,eliminarUsuarios_required, verUsuarios_required, crearRoles_required, modificarRoles_required, eliminarRoles_required, verRoles_required, verPermisos_required, crearProyectos_required, verItems_required, crearFases_required, modificarFases_required, eliminarFases_required
from ..decorators import crearComites_required,modificarProyectos_required, eliminarProyectos_required, verProyectos_required, crearComites_required, modificarComites_required, eliminarComites_required, verComites_required, verMiembrosComites_required, crearItems_required, modificarItems_required,eliminarItems_required, verFases_required

from ..modelos import LineaBase, HistorialLineaBase,Proyecto, Fase, Comite, User
from .forms_gdc import CrearLBForm, ComiteForm, LineaBaseForm, UserxComiteForm, BorrarComiteForm, CrearComiteForm

cambios = Blueprint('cambios', __name__, url_prefix='/cambios')
#COMITE

@cambios.route('/comites')
@login_required
#@verComites_required
def comites():
    """Funcion que lista los comites existentes en el sistema"""
    comites = Comite.query.all()
    return render_template('cambios/comites.html', comites=comites, active='comites')


@cambios.route('/ProyectosLB')
@login_required
#@verComites_required
def proyectosLB():
    """Funcion que lista los proyectos que pueden tener linea base """
    #proyectosLB = Proyecto.query.all()
    #Le pasamos solamente los proyectos en el que usuario actual participa
    proyectos=current_user.getProyectos()
    #debe filtra que sea lider en ese proyecto tambien
    
    return render_template('cambios/proyectosLB.html', proyectos=proyectos)

@cambios.route('/crearLB/<proyecto_id>/<fase_id>', methods=['GET', 'POST'])
@login_required
def crearLB(proyecto_id, fase_id):
    """Funcion que permite crear una Linea Base"""
    fase = Fase.query.filter_by(id=fase_id).first_or_404()
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    
    form = CrearLBForm(next=request.args.get('next'))
    
    
    if form.validate_on_submit():
        lineaBase = LineaBase()
        lineaBase.nombre = form.nombre.data
        lineaBase.fase_id = fase.id
        
        db.session.add(lineaBase)
        db.session.commit()
        
        flash('Linea Base creada.', 'success')
        return redirect(url_for('cambios.lineasBasexproyecto',proyecto_id=proyecto_id))
    return render_template('cambios/crearLineaBase.html', proyecto=proyecto, fase=fase, form=form)
       
    
@cambios.route('/crearComite', methods=['GET', 'POST'])
@login_required
#@crearComites_required
def crearComite():
    """Funcion que permite la creacion de un comite"""
    proyectos = Proyecto.query.filter_by(comite=None)
    form = CrearComiteForm(next=request.args.get('next'))
    form.proyecto_id.choices = [(h.id, h.nombre) for h in proyectos ]
       
    if form.validate_on_submit():      
        comite = Comite()
        proyecto = Proyecto.query.filter_by(id=form.proyecto_id.data).first_or_404()
        lider = proyecto.lider_proyecto
        user = User.query.filter_by(id=lider).first_or_404()
        comite.proyecto_id = proyecto.id
        comite.usuarioPorComite = [user]
        comite.nombre = form.nombre.data
        comite.descripcion = form.descripcion.data

        db.session.add(comite)
        db.session.commit()
        
        flash('Comite creado.', 'success')
        return redirect(url_for('cambios.comites'))
       
    return render_template('cambios/crearComite.html', form=form)

@cambios.route('/buscarComite')
@login_required
#@verComites_required
def buscarComite():
    """FUncion que busca un comite por nombre"""
    keywords = request.args.get('keywords', '').strip()
    pagination=None   
       
    if keywords:
        page = int(request.args.get('page', 1))
        pagination= Comite.search(keywords).paginate(page,1)
    else:
        flash('Por favor, ingrese dato a buscar','error')
    return render_template('index/buscarComite.html', pagination=pagination , keywords=keywords)


@cambios.route('/comite/<comite_id>', methods=['GET', 'POST'])
@login_required
#@modificarComites_required
def comite(comite_id):
    """Funcion que permite editar un comite"""
    comite = Comite.query.filter_by(id=comite_id).first_or_404()
    form = ComiteForm(obj=comite, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(comite)

        db.session.add(comite)
        db.session.commit()

        flash('Comite actualizado.', 'success')
        return redirect(url_for('cambios.comites'))

    return render_template('cambios/comite.html', comite=comite, form=form)

@cambios.route('/borrarComite/<comite_id>', methods=['GET', 'POST'])
@login_required
#@eliminarComites_required
def borrarComite(comite_id):
    """Funcion que permite la eliminacion de un comite"""
    comite = Comite.query.filter_by(id=comite_id).first_or_404()
    form = BorrarComiteForm(obj=comite, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(comite)

        db.session.delete(comite)
        db.session.commit()

        flash('Comite eliminado.', 'success')
        return redirect(url_for('cambios.comites'))

    return render_template('cambios/borrarComite.html', comite=comite, form=form)

@cambios.route('/usuariosxcomite/Comite<comite_id>/Usuario<user_id>', methods=['GET', 'POST'])
@login_required
#@desasignarMiembro_required
def desasignarMiembro(comite_id, user_id):
    """Funcion que permite desasignar a un usuario de un comite"""
    miembroDesasignar = User.query.filter_by(id=user_id).first_or_404()
    comite = Comite.query.filter_by(id=comite_id).first_or_404()
    proyecto = comite.getProyecto()
    form = UserxComiteForm(obj=user, next=request.args.get('next'))
    miembrosAsignados = comite.usuarioPorComite
    
    for item in miembrosAsignados:
        if miembroDesasignar.id == proyecto.lider_proyecto:
            flash('El usuario es Lider del proyecto, no puede ser desasignado.', 'error')
            return redirect(url_for('cambios.usuariosxcomite', comite_id=comite.id))
        if item == miembroDesasignar:
            comite.usuarioPorComite.remove(item)
            db.session.add(comite)
            db.session.commit()
            flash('Miembro desasignado.', 'success')
            return redirect(url_for('cambios.usuariosxcomite', comite_id=comite.id))
    
    return render_template('cambios/usuariosxcomite.html', comite=comite, form=form, users=miembrosAsignados)

@cambios.route('/usuariosxcomite/<comite_id>', methods=['GET', 'POST'])
@login_required
#@verMiembrosComites_required
def usuariosxcomite(comite_id):
    """Funcion que asigna los usuarios de un proyecto a un comite"""
    comite = Comite.query.filter_by(id=comite_id).first_or_404()
    proyecto = Proyecto.query.filter_by(id=comite.proyecto_id).first_or_404()
    form = UserxComiteForm(obj=comite, next=request.args.get('next'))
    usuariosAsignados = comite.usuarioPorComite
    todosUsuarios = proyecto.usuarioPorProyecto
#    todosUsuarios = User.query.all()
    UsuariosAsignar = [item for item in todosUsuarios if item not in usuariosAsignados]
    listaUsers = []
    for userAsig in usuariosAsignados:
        listaUsers.append(userAsig.id)
    
    form.usuarioPorComite.choices = [(h.id, h.nombre) for h in UsuariosAsignar ]
    
    if form.validate_on_submit():       
        listaTotal = form.usuarioPorComite.data
        for userAsig in listaUsers:
            listaTotal.append(userAsig)
        for userID in listaTotal:
            user = User.query.filter_by(id=userID).first()
            comite.usuarioPorComite.append(user)            
            
        db.session.add(comite)
        db.session.commit()
       
        flash('Miembro asignado.', 'success')
        return redirect(url_for('cambios.usuariosxcomite', comite_id=comite.id))
    
    return render_template('cambios/usuariosxcomite.html', comite=comite, form=form, users=usuariosAsignados)  



@cambios.route('/lineaBasexproyecto/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def lineaBasexproyecto(proyecto_id):
    """Funcion que lista las lineas base de un Proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    fases = proyecto.fases
    
    listaDeLB = []
    for fase in fases:
        faseElegida = Fase.query.filter_by(id=fase.id).first_or_404()
        lb = faseElegida.lineaBase
        for linea in lb:
            lineaBase = LineaBase.query.filter_by(id=linea.id).first_or_404()
            listaDeLB.append(lineaBase)
    
    return render_template('cambios/lineasbasexproyecto.html', proyecto=proyecto, fases=fases, lineasBases=listaDeLB, active='Lineas Base')


@cambios.route('/historialxlineabase/<lineabase_id>', methods=['GET', 'POST'])
@login_required
def historialxlineabase(lineabase_id):
    """Funcion que lista el historial de un Item"""
    lineabase = LineaBase.query.filter_by(id=lineabase_id).first_or_404()
    todosHistoriales = HistorialLineaBase.query.all()
    
    historiales=[]
    for historial in todosHistoriales:
        if historial.lineaBase_id==lineabase.id:
            historiales.append(historial)
    return render_template('cambios/historialxlineabase.html', lineabase=lineabase, historiales=historiales)


@cambios.route('/lineaBasexproyecto/<proyecto_id>/<lineabase_id>', methods=['GET', 'POST'])
@login_required
#@modificarProyectos_required
def lineaBase(proyecto_id, lineabase_id):
    """Funcion que permite editar una Linea Base"""
    lineaBase = LineaBase.query.filter_by(id=lineabase_id).first_or_404()
    form = LineaBaseForm(obj=lineaBase, next=request.args.get('next'))
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    #fases = proyecto.fases

    if form.validate_on_submit():
        form.populate_obj(lineaBase)

        db.session.add(lineaBase)
        db.session.commit()

        flash('Linea Base actualizado.', 'success')
        return redirect(url_for('cambios.lineaBasexproyecto', proyecto_id=proyecto.id, lineabase_id=lineaBase.id))

    return render_template('cambios/lineaBase.html', proyecto=proyecto, lineabase=lineaBase, form=form)

from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user

from ..extensions import db
from ..decorators import *

from ..modelos import *
from .forms_gdc import *

cambios = Blueprint('cambios', __name__, url_prefix='/cambios')
#COMITE

@cambios.route('/comites')
@login_required
#@verComites_required
def comites():
    """Funcion que lista los comites existentes en el sistema"""
    comites = Comite.query.all()
    return render_template('cambios/comites.html', comites=comites, active='comites')

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
    form = UserxComiteForm(obj=user, next=request.args.get('next'))
    miembrosAsignados = comite.usuarioPorComite
    
    for item in miembrosAsignados:
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
    
    return render_template('cambios/lineaBasexproyecto.html', proyecto=proyecto, fases=fases, lineasBases=listaDeLB, active='Lineas Base')

@cambios.route('/crearLineaBase/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def crearLineaBase(proyecto_id):
    """Funcion que permite instanciar una Linea Base de una Fase"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    fases = Fase.query.filter_by(proyecto_id=proyecto_id)
    form = CrearLineaBaseForm(next=request.args.get('next'))
    form.fase_id.choices = [(h.id, h.nombre) for h in fases ]
    
    if form.validate_on_submit():
        lineabase = LineaBase()
        fase = Fase.query.filter_by(id=form.fase_id.data).first_or_404()
        lineabase.numero_lb = form.numero_lb.data
        lineabase.descripcion = form.descripcion.data
        lineabase.fase_id = fase.id
        
        db.session.add(lineabase)
        db.session.commit()
        
        historial = HistorialLineaBase()
        historial.lineaBase_id = lineabase.id
        historial.descripcion= current_user.nombre+" creo la Linea Base " +str(lineabase.numero_lb)+ " de la Fase " +str(lineabase.fase_id)
        
        db.session.add(historial)
        db.session.commit()
        
        flash('Linea Base creada.', 'success')
        return redirect(url_for('cambios.lineaBasexproyecto',proyecto_id=proyecto.id))
    
    return render_template('cambios/crearLineaBase.html', proyecto=proyecto, form=form)

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
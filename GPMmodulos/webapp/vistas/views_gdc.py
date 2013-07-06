from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user

from ..extensions import db
from ..decorators import crearUsuarios_required, modificarUsuarios_required,eliminarUsuarios_required, verUsuarios_required, crearRoles_required, modificarRoles_required, eliminarRoles_required, verRoles_required, verPermisos_required, crearProyectos_required, verItems_required, crearFases_required, modificarFases_required, eliminarFases_required
from ..decorators import crearComites_required,modificarProyectos_required, eliminarProyectos_required, verProyectos_required, crearComites_required, modificarComites_required, eliminarComites_required, verComites_required, verMiembrosComites_required, crearItems_required, modificarItems_required,eliminarItems_required, verFases_required

from ..modelos import BLOQUEADO,APROBADO, CERRADA, Item, LineaBase, HistorialLineaBase,Proyecto, Fase, Comite, User
from .forms_gdc import AsignarItemsLBForm, CrearLBForm, ComiteForm, LineaBaseForm, UserxComiteForm, BorrarComiteForm, CrearComiteForm

#Librerias para dibujar el grafo
#import sys
#sys.path.append('..')
#sys.path.append('/usr/lib/graphviz/python/')
#sys.path.append('/usr/lib64/graphviz/python/')
#import gv
import pygraphviz as pgv
from pygraphviz import *


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
    """Funcion que lista los proyectositem.estado_id = BLOQUEADO  que pueden tener linea base """
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
        return redirect(url_for('cambios.lineaBasexproyecto',proyecto_id=proyecto_id))
    return render_template('cambios/crearLineaBase.html', proyecto=proyecto, fase=fase, form=form)
       
@cambios.route('/asignarItemsLB/<lineaBase_id>/', methods=['GET', 'POST'])
@login_required
def asignarItemsLB(lineaBase_id):
    """Funcion que permite asignar un item a una Linea Base"""
    lineaBase = LineaBase.query.filter_by(id=lineaBase_id).first_or_404()
    fase = Fase.query.filter_by(id=lineaBase.fase_id).first_or_404()
    
    form = AsignarItemsLBForm(obj=fase, next=request.args.get('next'))
    itemsDisponibles=[]
    itemsActuales = lineaBase.items
    for item in fase.items:
        if item not in itemsActuales and item.getEstado()!='bloqueado' and item.getEstado() != 'desaprobado':
            itemsDisponibles.append(item) #aca filtrar que el item debe estar aprobado
          
    form.items.choices = [(h.id, h.nombre) for h in itemsDisponibles ]
    
    if form.validate_on_submit():       
        listaItemsSeleccionados=form.items.data  # trae el id de los item que selecciono
                    
        for itemAsig in itemsActuales:    # a la lista de items que ya tiene, le agrega lo que selecciono
            listaItemsSeleccionados.append(itemAsig.id)
                     
        for itemID in listaItemsSeleccionados:
            item=Item.query.filter_by(id=itemID).first_or_404()
            item.setEstado(BLOQUEADO) #Se bloquea el item
            lineaBase.items.append(item)
        lineaBase.estado_id = CERRADA
        fase.actualizarEstado()
        
        db.session.add(fase)    
        db.session.add(lineaBase)
        db.session.commit()
       
        flash('Items agregados.', 'success')
        return redirect(url_for('cambios.lineaBasexproyecto', proyecto_id=fase.proyecto_id))
       
    return render_template('cambios/asignarItemsLB.html', lineaBase=lineaBase, form=form)

@cambios.route('/desasignarItemsLB/<lineaBase_id>/<item_id>', methods=['GET', 'POST'])
@login_required
def desasignarItemsLB(lineaBase_id, item_id):
    """Funcion que permite desasignar un item de una Linea Base"""
    lineaBase = LineaBase.query.filter_by(id=lineaBase_id).first_or_404()
    item = Item.query.filter_by(id=item_id).first_or_404()
    fase = Fase.query.filter_by(id=lineaBase.fase_id).first_or_404()
    
    lineaBase.items.remove(item)
    item.setEstado(APROBADO)
    fase.actualizarEstado()
    
    db.session.add(lineaBase)
    db.session.add(fase)
    db.session.commit()
    
    flash ('Se ha quitado el item exitosamente', 'success')
    return redirect(url_for('cambios.lineaBasexproyecto', proyecto_id=item.proyecto_id))


    
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
    form = UserxComiteForm(obj=miembroDesasignar, next=request.args.get('next'))
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

@cambios.route('/reemplazarMiembro/Comite<comite_id>/<user_id>/<candidato_id>', methods=['GET', 'POST'])
@login_required
#@desasignarMiembro_required
def reemplazarMiembro(comite_id, user_id, candidato_id):
    comite = Comite.query.filter_by(id=comite_id).first_or_404()
    candidato = User.query.filter_by(id = candidato_id).first_or_404()
    usuario = User.query.filter_by(id = user_id).first_or_404()
    proyecto = Proyecto.query.filter_by(id =comite.proyecto_id).first_or_404()
    
    if proyecto.getUsuarioLider() == usuario:
        flash('Es Lider de Proyecto. No puede salir del comite.', 'error')
        return redirect(url_for('cambios.usuariosxcomite', comite_id=comite.id))
    
    comite.usuarioPorComite.append(candidato)
    comite.usuarioPorComite.remove(usuario)
    db.session.add(comite)
    db.session.commit()
    
    return redirect(url_for('cambios.usuariosxcomite', comite_id=comite.id))
    #desasignarMiembro(comite_id, user_id)
    
    




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
    
    return render_template('cambios/usuariosxcomite.html', proyecto=proyecto, comite=comite, form=form, users=usuariosAsignados)  



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

@cambios.route('/grafosItemsLB/<lineaBase_id>/', methods=['GET', 'POST'])
@login_required
def dibujarGrafoLB(lineaBase_id):
    """Funcion que permite asignar un item a una Linea Base"""
    lineaBase = LineaBase.query.filter_by(id=lineaBase_id).first_or_404()
    fase = Fase.query.filter_by(id=lineaBase.fase_id).first_or_404()
    
    desplazamiento_x = {}
    __index = 0
    for i in lineaBase.items:
        desplazamiento_x[i.id] = __index
        __index+=1
    # eje y
    desplazamiento_y = []
    for i in range(lineaBase.getNroItems()):
        desplazamiento_y.append(0)
    
    #####
    gr = pgv.AGraph(label= "Costo de la Linea Base: "+ str(lineaBase.getComplejidad()),directed=True)
    #gr.node_attr['shape']='circle'
    nodos= []
    id_nodos= []
    for nodo in lineaBase.items:
        if nodo.getEstado() != 'Eliminado':
            id_nodos.append(nodo.id)
            nodos.append(nodo)
    
    for nodo in nodos:
        item = nodo
        valor = str(item.id)+" : "+str(item.getComplejidad())
        index = desplazamiento_x[item.fase_id]
        posicion =  str(index*3.5)+','+str(90-desplazamiento_y[index]*2)
        desplazamiento_y[index] = desplazamiento_y[index] + 1
        color= 'white'
        if item.getMarcado() == 'Si':
            color= '#708090'
        gr.add_node(valor, label= item.getNombre()+" : "+  str(item.getComplejidad()), fillcolor=color, style="filled", pos=posicion, pin=True)
    
    gr.layout()
    gr.draw('webapp/static/grafos/grafo_item.png')
#    archivo= open('webapp/static/grafos/grafo_item.png','rb')
#    contenido= archivo.read()
#    archivo.close()
#    return Response(contenido)
   
    flash('Items dibujados.', 'success')
    return redirect(url_for('cambios.lineaBasexproyecto', proyecto_id=fase.proyecto_id))

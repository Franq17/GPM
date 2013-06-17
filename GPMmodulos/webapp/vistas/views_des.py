# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user

from ..extensions import db
from ..decorators import *

from ..modelos import *
from .forms_des import *

des = Blueprint('des', __name__, url_prefix='/des')


@des.route('/itemsxproyecto/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def itemsxproyecto(proyecto_id):
    """Funcion que lista los items de un Proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    itemsExistentes = proyecto.items
    return render_template('des/itemsxproyecto.html', proyecto=proyecto, items=itemsExistentes, active='Items')


@des.route('/crearItem/<proyecto_id>/<fase_id>', methods=['GET', 'POST'])
@login_required
def crearItem(proyecto_id, fase_id):
    """Funcion que permite instanciar un Item de un Proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    fase = Fase.query.filter_by(id=fase_id).first_or_404()
    tiposItem= TipoItem.query.filter_by(proyecto_id=proyecto_id)
    
    form = CrearItemForm(next=request.args.get('next'))
    form.tipoItem_id.choices = [(h.id, h.nombre) for h in tiposItem ]
    if form.validate_on_submit():
        item = Item()
        tipoItem = TipoItem.query.filter_by(id=form.tipoItem_id.data).first_or_404()
        item.nombre = form.nombre.data
        item.descripcion = form.descripcion.data
        item.proyecto_id = proyecto.id
        item.fase_id = fase.id
        item.tipoItem_id = tipoItem.id
        
        
        db.session.add(item)
        db.session.commit()
        
        historial = HistorialItem()
        historial.itemId=item.id
        historial.descripcion= current_user.nombre+" creo el item, con nombre: " + item.nombre
        
        db.session.add(historial)
        db.session.commit()
     
        
        flash('Item creado correctamente.', 'success')
        return redirect(url_for('des.fasesxproyecto', proyecto_id=proyecto.id))
        
    return render_template('des/crearItem.html', proyecto=proyecto, fase = fase, form=form)


@des.route('/IdItem<item_id>/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def item(proyecto_id, item_id):
    """Funcion que permite editar un item"""
    item = Item.query.filter_by(id=item_id).first_or_404()
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    form = ItemForm(obj=item, next=request.args.get('next'))
    if form.validate_on_submit():
        form.populate_obj(item)
        
        
        db.session.add(item)
        db.session.commit()

        historial = HistorialItem()
        historial.itemId=item.id
        historial.descripcion= current_user.nombre+" modifico el item." 
        
        db.session.add(historial)
        db.session.commit()
     
        flash('Item actualizado.', 'success')
        return redirect(url_for('des.itemsxproyecto',proyecto_id=proyecto.id))

    return render_template('des/item.html', item=item, proyecto=proyecto, form=form)

@des.route('/historialxitem/<item_id>', methods=['GET', 'POST'])
@login_required
def historialxitem(item_id):
    """Funcion que lista el historial de un Item"""
    item = Item.query.filter_by(id=item_id).first_or_404()
    todosHistoriales = HistorialItem.query.all()
    
    historiales=[]
    for historial in todosHistoriales:
        if historial.itemId==item.id:
            historiales.append(historial)
    return render_template('des/historialxitem.html', item=item, historiales=historiales)

@des.route('/IT<item_id>/PR<proyecto_id>', methods=['GET', 'POST'])
@login_required
def crearSolicitud(item_id, proyecto_id):
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    comite = proyecto.comite
    item = Item.query.filter_by(id=item_id).first_or_404()
    usuariosComite = comite.usuarioPorComite
    itemsExistentes = proyecto.items
    
    print "Recibie$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    print item_id
        
    
    solicitud = Solicitud()
    solicitud.comite_id = comite.id
    solicitud.item_id = item_id
    db.session.add(solicitud)
    db.session.commit()
    
    for usuario in usuariosComite:
        usuario.solicitudPorUsuario.append(solicitud)
        
        print "Solicitu de$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        print solicitud.item_id
        
        db.session.add(usuario)
        db.session.commit()
    
    flash('Solicitud enviada correctamente.', 'success')
   
    return render_template('des/itemsxproyecto.html', proyecto=proyecto, items=itemsExistentes, active='Items')


@des.route('/fasesxproyecto/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def fasesxproyecto(proyecto_id):
    """Funcion que lista las fases de un Proyecto"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    fases = proyecto.fases
    #cabeceras=[]
    #for fase in fasesExistentes:
    #   cabeceras.append((fase.nombre, proyecto.id, fase.id ))
    return render_template('des/fases.html', proyecto=proyecto, fases=fases, active='Fases')

@des.route('/IdF<fase_id>/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def fase(proyecto_id, fase_id):
    """Funcion que permite ver contenidos de una fase"""
    fase = Fase.query.filter_by(id=fase_id).first_or_404()
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    items =  fase.getItems(proyecto.id)
    return render_template('des/fase.html', fase=fase, proyecto=proyecto, items=items, active='Fases', active1='Fase uno')



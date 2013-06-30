from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user

from ..modelos import ItemPorProyectoReporte, HistorialPorItemReporte, HistorialItem, Item, Proyecto, Fase
from .forms_reportes import ReporteItemsxProyectoForm, ReporteHistorialxItemPaso1Form, ReporteHistorialxItemPaso2Form 

from geraldo.generators import PDFGenerator

reportes = Blueprint('reportes', __name__, url_prefix='/reportes')

@reportes.route('/itemsxproyecto', methods=['GET', 'POST'])
@login_required
def itemsxproyecto():
    """Funcion que crea un reporte PDF"""
    proyectos = Proyecto.query.all()
    form = ReporteItemsxProyectoForm(next=request.args.get('next'))
    form.proyecto_id.choices = [(h.id, h.nombre) for h in proyectos ]
    
    if form.validate_on_submit():
        proyecto = Proyecto.query.filter_by(id=form.proyecto_id.data).first_or_404()
        
        listaItems=[]
        for item in proyecto.items:
            fase = Fase.query.filter_by(id=item.fase_id).first_or_404()
            listaItems.append({'id': item.id,'nombre': item.nombre, 'estado': item.getEstado(), 'fase':fase.nombre})
        
        listaItems.sort(lambda a,b: cmp(a['fase'], b['fase']))
        my_report = ItemPorProyectoReporte(queryset=listaItems)
        my_report.generate_by(PDFGenerator, filename='/home/franq/Escritorio/items_'+proyecto.nombre+'.pdf')
        
        flash('Reporte creado exitosamente en su Escritorio', 'success')
        return redirect(url_for('reportes.itemsxproyecto'))
    return render_template('reportes/itemsxproyecto.html', form=form)


@reportes.route('/historialxitemPaso1', methods=['GET', 'POST'])
@login_required
def historialxitemPaso1():
    """Funcion que crea un reporte PDF del historial de un item"""
    proyectos = Proyecto.query.all()
    form = ReporteHistorialxItemPaso1Form(next=request.args.get('next'))
    form.proyecto_id.choices = [(h.id, h.nombre) for h in proyectos ]
    
    if form.validate_on_submit():
        proyecto_id = form.proyecto_id.data
        return redirect(url_for('reportes.historialxitemPaso2', proyecto_id=proyecto_id))
    return render_template('reportes/historialxitemPaso1.html', form=form)


@reportes.route('/historialxitemPaso2/<proyecto_id>', methods=['GET', 'POST'])
@login_required
def historialxitemPaso2(proyecto_id):
    """Funcion que crea un reporte PDF del historial de un item"""
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first_or_404()
    
    form = ReporteHistorialxItemPaso2Form(next=request.args.get('next'))
    form.item_id.choices = [(h.id, h.nombre) for h in proyecto.items ]
    
    if form.validate_on_submit():
        item = Item.query.filter_by(id=form.item_id.data).first_or_404()
        todosHistoriales = HistorialItem.query.all()
         
        historiales=[]
        for historial in todosHistoriales:
            if historial.itemId==item.id:
                historiales.append(historial)
        
        listaHistorial=[]
        for fila in historiales:
            listaHistorial.append({'id': fila.itemId,'descripcion': fila.descripcion, 'fecha':fila.fecha})
        
        my_report = HistorialPorItemReporte(queryset=listaHistorial)
        my_report.generate_by(PDFGenerator, filename='/home/franq/Escritorio/historial_'+item.nombre+'.pdf')
        
        flash('Reporte creado exitosamente en su Escritorio', 'success')
        return redirect(url_for('reportes.historialxitemPaso1'))
    return render_template('reportes/historialxitemPaso2.html', proyecto_id=proyecto_id, form=form)
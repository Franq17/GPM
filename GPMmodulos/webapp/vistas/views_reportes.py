from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user

from ..modelos import ItemPorProyectoReporte, HistorialPorItemReporte, SolicitudesPorProyectoReporte, HistorialItem, Item, LineaBase, Proyecto, Fase, Solicitud, User
from .forms_reportes import ReporteItemsxProyectoForm, ReporteHistorialxItemPaso1Form, ReporteHistorialxItemPaso2Form, ReporteSolicitudesxProyectoForm 

from geraldo.generators import PDFGenerator

reportes = Blueprint('reportes', __name__, url_prefix='/reportes')

@reportes.route('/itemsxproyecto', methods=['GET', 'POST'])
@login_required
def itemsxproyecto():
    """Funcion que crea un reporte PDF"""
    if current_user.comprobarPermiso('administrador'):
        proyectos = Proyecto.query.all()
    elif current_user.comprobarPermiso('liderProyecto'):
        proyectos = current_user.getProyectosDeLider()
    
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
        my_report.generate_by(PDFGenerator, filename='/home/adolfo/Escritorio/items_'+proyecto.nombre+'.pdf')
        
        flash('Reporte creado exitosamente en su Escritorio', 'success')
        return redirect(url_for('reportes.itemsxproyecto'))
    return render_template('reportes/itemsxproyecto.html', form=form)


@reportes.route('/historialxitemPaso1', methods=['GET', 'POST'])
@login_required
def historialxitemPaso1():
    """Funcion que crea un reporte PDF del historial de un item"""
    if current_user.comprobarPermiso('administrador'):
        proyectos = Proyecto.query.all()
    elif current_user.comprobarPermiso('liderProyecto'):
        proyectos = current_user.getProyectosDeLider()

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
        historiales = HistorialItem.query.filter_by(itemId=item.id)
         
        #historiales=[]
        #for historial in todosHistoriales:
        #    if historial.itemId==item.id:
        #        historiales.append(historial)
        
        listaHistorial=[]
        for fila in historiales:
            listaHistorial.append({'id': fila.itemId,'descripcion': fila.descripcion, 'fecha':fila.fecha})
        
        my_report = HistorialPorItemReporte(queryset=listaHistorial)
        my_report.generate_by(PDFGenerator, filename='/home/adolfo/Escritorio/historial_'+item.nombre+'.pdf')
        
        flash('Reporte creado exitosamente en su Escritorio', 'success')
        return redirect(url_for('reportes.historialxitemPaso1'))
    return render_template('reportes/historialxitemPaso2.html', proyecto_id=proyecto_id, form=form)


@reportes.route('/solicitudesxproyecto', methods=['GET', 'POST'])
@login_required
def solicitudesxproyecto():
    """Funcion que crea un reporte PDF"""
    proyectos = Proyecto.query.all()
    form = ReporteSolicitudesxProyectoForm(next=request.args.get('next'))
    form.proyecto_id.choices = [(h.id, h.nombre) for h in proyectos ]
    
    if form.validate_on_submit():
        proyecto = Proyecto.query.filter_by(id=form.proyecto_id.data).first_or_404()
        comite = proyecto.comite
        
        if comite is None:
            flash('El proyecto no cuenta con un Comite de cambios.', 'error')
            return redirect(url_for('reportes.solicitudesxproyecto'))
        listaSolicitudes = Solicitud.query.filter_by(comite_id=comite.id)
        
        listaImprimir = []
        for solicitud in listaSolicitudes:
            
            item = Item.query.filter_by(id=solicitud.item_id).first_or_404()
            lineaBase = LineaBase.query.filter_by(id=item.lineaBase_id).first_or_404()
            solicitante = User.query.filter_by(id=solicitud.solicitante).first_or_404()
            if solicitud.estado == 0:
                estadoSolicitud = "Sin votos"
            if solicitud.estado == 1:
                estadoSolicitud = "En curso"
            if solicitud.estado == 2:
                estadoSolicitud = "Finalizado"
                
            listaImprimir.append({'lineaBase': lineaBase.nombre, 'item': item.nombre,'solicitante': solicitante.nombre, 'estado': estadoSolicitud})
        
        #listaItems.sort(lambda a,b: cmp(a['fase'], b['fase']))
        my_report = SolicitudesPorProyectoReporte(queryset=listaImprimir)
        my_report.generate_by(PDFGenerator, filename='/home/adolfo/Escritorio/solicitudes_'+proyecto.nombre+'.pdf')
        
        flash('Reporte creado exitosamente en su Escritorio', 'success')
        return redirect(url_for('reportes.solicitudesxproyecto'))
    return render_template('reportes/solicitudCambio.html', form=form)

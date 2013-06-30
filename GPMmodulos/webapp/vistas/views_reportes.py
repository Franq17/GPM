from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user

from ..extensions import db
from ..decorators import crearUsuarios_required, modificarUsuarios_required,eliminarUsuarios_required, verUsuarios_required, crearRoles_required, modificarRoles_required, eliminarRoles_required, verRoles_required, verPermisos_required, crearProyectos_required, verItems_required, crearFases_required, modificarFases_required, eliminarFases_required
from ..decorators import crearComites_required,modificarProyectos_required, eliminarProyectos_required, verProyectos_required, crearComites_required, modificarComites_required, eliminarComites_required, verComites_required, verMiembrosComites_required, crearItems_required, modificarItems_required,eliminarItems_required, verFases_required

from ..modelos import ItemPorProyectoReporte, BLOQUEADO, CERRADA, Item, LineaBase, HistorialLineaBase,Proyecto, Fase, Comite, User
from .forms_gdc import AsignarItemsLBForm, CrearLBForm, ComiteForm, LineaBaseForm, UserxComiteForm, BorrarComiteForm, CrearComiteForm
from .forms_reportes import ReporteItemsxProyectoForm, ReporteHistorialxItemForm

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
        
        my_report = ItemPorProyectoReporte(queryset=listaItems)
        my_report.generate_by(PDFGenerator, filename='/home/adolfo/Escritorio/items_'+proyecto.nombre+'.pdf')
        
        flash('Reporte creado exitosamente en su Escritorio', 'success')
        return redirect(url_for('reportes.itemsxproyecto'))
    return render_template('reportes/itemsxproyecto.html', form=form)

@reportes.route('/historialxitem', methods=['GET', 'POST'])
@login_required
def historialxitem():
    """Funcion que crea un reporte PDF"""
    proyectos = Proyecto.query.all()
    form = ReporteHistorialxItemForm(next=request.args.get('next'))
    form.proyecto_id.choices = [(h.id, h.nombre) for h in proyectos ]
    
    if form.validate_on_submit():
        #lineaBase = LineaBase()
        #lineaBase.nombre = form.nombre.data
        #lineaBase.fase_id = fase.id
        
        #db.session.add(lineaBase)
        #db.session.commit()
        
        flash('Reporte creado correctamente en su Escritorio', 'success')
        return redirect(url_for('reportes.historialxitem'))
    return render_template('reportes/historialxitem.html', form=form)


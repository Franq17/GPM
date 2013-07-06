# -*- coding: utf-8 -*-

from flask_wtf import Form
from flask_wtf import (HiddenField, SelectField, SubmitField)

class ReporteItemsxProyectoForm(Form):
    next = HiddenField()
    proyecto_id = SelectField(u'Seleccione un Proyecto:', coerce=int,)
    submit = SubmitField(u'Crear Reporte')
    
class ReporteHistorialxItemPaso1Form(Form):      
    next = HiddenField()
    proyecto_id = SelectField(u'Seleccione un Proyecto:', coerce=int,)
    submit = SubmitField(u'Continuar >')

class ReporteHistorialxItemPaso2Form(Form):      
    next = HiddenField()
    item_id = SelectField(u'Seleccione un Item:', coerce=int,)
    submit = SubmitField(u'Crear Reporte')
    
class ReporteSolicitudesxProyectoForm(Form):
    next = HiddenField()
    proyecto_id = SelectField(u'Seleccione un Proyecto:', coerce=int,)
    submit = SubmitField(u'Crear Reporte')
from sqlalchemy import Column, types
try:
    from sqlalchemy.ext.mutable import Mutable
except ImportError:
    from sqlalchemy.types import MutableType as Mutable
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin


from geraldo import Report, ReportBand, DetailBand, SystemField, Label, ObjectValue
from geraldo.utils import cm, BAND_WIDTH, TA_CENTER, TA_RIGHT
from geraldo.generators import PDFGenerator



family = [
    {'name': 'Leticia', 'age': 29, 'weight': 55.7, 'genre': 'female', 'status': 'parent'},
    {'name': 'Marinho', 'age': 28, 'weight': 76, 'genre': 'male', 'status': 'parent'},
    {'name': 'Tarsila', 'age': 4, 'weight': 16.2, 'genre': 'female', 'status': 'child'},
    {'name': 'Linus', 'age': 0, 'weight': 1.5, 'genre': 'male', 'status': 'child'},
    {'name': 'Mychelle', 'age': 19, 'weight': 50, 'genre': 'female', 'status': 'nephew'},
    {'name': 'Mychell', 'age': 17, 'weight': 55, 'genre': 'male', 'status': 'niece'},
]

class MyFamilyReport(Report):
    title = 'Lista de Clientes'
    
    #cuerpo que muestra los datos en si 
    class band_detail(DetailBand):
        height = 0.7 * cm
        elements = [
            ObjectValue(expression='name', left=0.5 * cm),
            ObjectValue(expression='age', left=5 * cm),
            ObjectValue(expression='weight', left=6.5 * cm),
        ]
        borders = {'bottom': True}
    #cabecera pagina
    class band_page_header(ReportBand):
        height = 1.3 * cm
        elements = [
            SystemField(expression='%(report_title)s', top=0.1 * cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1 * cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            Label(text="Nombre", top=0.8 * cm, left=0.5 * cm),
            Label(text="Edad", top=0.8 * cm, left=5 * cm),
            Label(text="Altura", top=0.8 * cm, left=6.5 * cm),
        ]
        borders = {'all': True}
    #Pie de pagina    
    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='GPM', top=0.1*cm),
            SystemField(expression='Impreso %(now:%Y, %b %d)s a las %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}


my_report = MyFamilyReport(queryset=family)
my_report.generate_by(PDFGenerator, filename='/home/adolfo/Escritorio/family.pdf')

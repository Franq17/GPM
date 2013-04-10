# -*- coding: utf-8 -*-
#   Proyecto GPM: Generic Project Manager
#   Revisado el 6 Abril de 2013, por Francisco Quiñonez (franqur17@gmail.com)
#   Controlado:
#      - Adolfo Salas
#      - Pablo Sanchez

r"""Module doctest -- a framework for running examples in docstrings.

Prueba de una funcion Grande
"""


import os

from flask.ext.script import Manager

from webapp import create_app
from webapp.extensions import db
from webapp.user import User, UserDetail, ADMIN, USER, ACTIVE
from webapp.project import Project, INICIADO 



app = create_app()
manager = Manager(app)
project_root_path = os.path.join(os.path.dirname(app.root_path))

@manager.command
def test():
    """Run tests."""
    
    os.system("nosetests")

 
    
@manager.command
def initdb():
    """Init/reset database.
    Clase encargada de iniciar y reiniciar la base de datos"""

    db.drop_all()
    db.create_all()
    # Init/reset data.

    admin = User(
            name=u'admin', 
            email=u'admin@example.com', 
            password=u'123456', 
            role_id=ADMIN,
            status_id=ACTIVE,
            user_detail=UserDetail(
                nameReal=u'administrador',
				apellido=u'administrador',
				location=u'Hangzhou',
                document=4441459,                  
                descripcion=u'admin Guy is ... hmm ... just a admin guy.'),
            )
    lider = User(
            name=u'lider', 
            email=u'lider@example.com', 
            password=u'123456', 
            role_id=USER,
            status_id=ACTIVE,
            user_detail=UserDetail(
                nameReal=u'Adolfo',
				apellido=u'Salas',
                location=u'Hangzhou', 
				document=4345435,
                descripcion=u'lider Guy is ... hmm ... just a demo guy.'),
            )             
    usuario = User(
            name=u'usuario', 
            email=u'usuario@example.com', 
            password=u'123456', 
            role_id=USER,
            status_id=ACTIVE,
            user_detail=UserDetail(
                nameReal=u'Francisco',
				apellido=u'quiñonez',
                location=u'Hangzhou', 
				document=4575,
                descripcion=u'usuario is ... hmm ... just a demo guy.'),
			)
    ejemplo = Project(
            nombre=u'ejemplo1',
            estado_id=INICIADO,
            numero_fases=3,
            lider_proyecto="usuario",
            complejidad_total=20,
            descripcion=u'proyecto loco probando',
            )
                
    db.session.add(admin)
    db.session.add(lider) 
    db.session.add(usuario)
    db.session.add(ejemplo)    
    db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()

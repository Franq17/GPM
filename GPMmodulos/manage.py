# -*- coding: utf-8 -*-

import os

from flask_script import Manager

from webapp import create_app
from webapp.extensions import db
from webapp.modelos import User, Rol, Permiso, Proyecto, INICIADO, Comite, ADMIN, USER, ACTIVE


app = create_app()
manager = Manager(app)
project_root_path = os.path.join(os.path.dirname(app.root_path))

@manager.command
def test():
    """Run tests."""
    
    os.system("nosetests")
    
    
@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()
    # Init/reset data.

    
    admin = User(
            name=u'admin',
            nombre=u'Jorge',
            apellido=u'Zalazar', 
            email=u'admin@example.com', 
            password=u'123456', 
            role_id=ADMIN,
            status_id=ACTIVE
            )
    
    lider = User(
            name=u'lider',
            nombre=u'Luis',
            apellido=u'Baez',
            email=u'lider@example.com', 
            password=u'123456', 
            role_id=USER,
            status_id=ACTIVE
            )
            
    usuario = User(
            name=u'usuario',
            nombre=u'Marta',
            apellido=u'Candia', 
            email=u'usuario@example.com', 
            password=u'123456', 
            role_id=USER,
            status_id=ACTIVE
            )
             
    permiso1 = Permiso(nombre=u'crearUsuarios',descripcion=u'permite crear usuarios')
    permiso2 = Permiso(nombre=u'modificarUsuarios',descripcion=u'permite modificar usuarios')
    permiso3 = Permiso(nombre=u'eliminarUsuarios',descripcion=u'permite eliminar usuarios')
    permiso4 = Permiso(nombre=u'crearRoles',descripcion=u'permite crear roles')
    
    rol_admin = Rol(nombre=u'admin',descripcion=u'rol del administrador', permisoPorRol=[permiso1,permiso2,permiso3,permiso4])
    rol_lider = Rol(nombre=u'lider',descripcion=u'rol del lider')
    rol_usuario = Rol(nombre=u'usuario',descripcion=u'rol del usuario')
    
    comite_usuario = Comite(nombre=u'Grupo7', descripcion=u'Comite del proyecto1', usuarioPorComite=[usuario,lider])
    

    db.session.add(admin)
    db.session.add(lider) 
    db.session.add(usuario)
    db.session.add(rol_admin)
    db.session.add(rol_lider)
    db.session.add(rol_usuario)
    db.session.add(comite_usuario)
    

    db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()

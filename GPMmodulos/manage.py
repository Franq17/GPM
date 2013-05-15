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
    """Init/reset Base de Datos."""

    db.drop_all()
    db.create_all()
    # Init/reset data.

    
    #*******************Permisos de Usuarios*****************************         
    permiso1 = Permiso(nombre=u'crearUsuarios',descripcion=u'permite crear usuarios')
    permiso2 = Permiso(nombre=u'modificarUsuarios',descripcion=u'permite modificar usuarios')
    permiso3 = Permiso(nombre=u'eliminarUsuarios',descripcion=u'permite eliminar usuarios')
    permiso4 = Permiso(nombre=u'verUsuarios',descripcion=u'permite ver lista de usuarios')
    
    #*******************Permisos de Roles*****************************
    permiso5 = Permiso(nombre=u'crearRoles',descripcion=u'permite crear roles')
    permiso6 = Permiso(nombre=u'modificarRoles',descripcion=u'permite modificar roles')
    permiso7 = Permiso(nombre=u'eliminarRoles',descripcion=u'permite eliminar roles')
    permiso8 = Permiso(nombre=u'verRoles',descripcion=u'permite ver Roles existentes')
    
    permiso9 = Permiso(nombre=u'verPermisos',descripcion=u'permite ver Permisos existentes')
        
    #*******************Permisos de Proyectos*****************************
    permiso10 = Permiso(nombre=u'crearProyectos',descripcion=u'permite crear Proyectos')
    permiso11 = Permiso(nombre=u'modificarProyectos',descripcion=u'permite modificar Proyectos')
    permiso12 = Permiso(nombre=u'eliminarProyectos',descripcion=u'permite eliminar Proyectos')
    permiso13 = Permiso(nombre=u'verProyectos',descripcion=u'permite ver Proyectos existentes')
    
    #*******************Permisos de Comites*****************************
    permiso14 = Permiso(nombre=u'crearComites',descripcion=u'permite crear Comites')
    permiso15 = Permiso(nombre=u'modificarComites',descripcion=u'permite modificar Comites')
    permiso16 = Permiso(nombre=u'eliminarComites',descripcion=u'permite eliminar Comites')
    permiso17 = Permiso(nombre=u'verComites',descripcion=u'permite ver Comites existentes')
    
    permiso18 = Permiso(nombre=u'verMiembrosComites',descripcion=u'permite ver los miembros de un Comite')
    
    #*******************Permisos de Items*****************************
    permiso19 = Permiso(nombre=u'crearItems',descripcion=u'permite crear Items')
    permiso20 = Permiso(nombre=u'modificarItems',descripcion=u'permite modificar Items')
    permiso21 = Permiso(nombre=u'eliminarItems',descripcion=u'permite eliminar Items')
    permiso22 = Permiso(nombre=u'verItems',descripcion=u'permite ver Items existentes')
    
    #*******************Permisos de Fases*****************************
    permiso23 = Permiso(nombre=u'crearFases',descripcion=u'permite crear Fases')
    permiso24 = Permiso(nombre=u'modificarFases',descripcion=u'permite crear Fases')
    permiso25 = Permiso(nombre=u'eliminarFases',descripcion=u'permite crear Fases')
    permiso26 = Permiso(nombre=u'verFases',descripcion=u'permite crear Fases')
    
    rol_admin = Rol(nombre=u'administrador',
                    descripcion=u'rol del administrador', 
                    permisoPorRol=[permiso1,permiso2,permiso3,permiso4,permiso5,
                                   permiso6,permiso7,permiso8,permiso9,permiso10,
                                   permiso11,permiso12,permiso13,permiso14,permiso15,
                                   permiso16,permiso17,permiso18,permiso19,permiso20,
                                   permiso21,permiso22,permiso23,permiso24,permiso25,
                                   permiso26])
    
    rol_admin_usuarios = Rol(nombre=u'administrador Usuarios',
                    descripcion=u'rol que solo administra usuarios', 
                    permisoPorRol=[permiso1,permiso2,permiso3,permiso4])
    
    rol_admin_comites = Rol(nombre=u'administrador Comites',
                    descripcion=u'rol que solo administra comites', 
                    permisoPorRol=[permiso14,permiso15,permiso16,permiso17,permiso18])
    
    
    rol_lider = Rol(nombre=u'lider',descripcion=u'rol del lider')
    rol_usuario = Rol(nombre=u'usuario',descripcion=u'rol del usuario')
    
    admin = User(
            name=u'admin',
            nombre=u'Adolfo',
            apellido=u'Salas', 
            email=u'admin@example.com', 
            password=u'123456',
            rolPorUsuario=[rol_admin], 
            role_id=ADMIN,
            status_id=ACTIVE
            )
    
    lider = User(
            name=u'lider',
            nombre=u'Francisco',
            apellido=u'Quiñonez',
            email=u'lider@example.com', 
            password=u'123456',
            rolPorUsuario=[rol_admin_usuarios], 
            role_id=USER,
            status_id=ACTIVE
            )
            
    usuario = User(
            name=u'usuario',
            nombre=u'Pablo',
            apellido=u'Sanchez', 
            email=u'usuario@example.com', 
            password=u'123456',
            rolPorUsuario=[rol_admin_comites], 
            role_id=USER,
            status_id=ACTIVE
            )
    
    db.session.add(admin)
    db.session.add(lider) 
    db.session.add(usuario)
    db.session.add(rol_admin)
    db.session.add(rol_lider)
    db.session.add(rol_usuario)
    db.session.add(rol_admin_usuarios)
    db.session.add(rol_admin_comites)
    
    

    db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()

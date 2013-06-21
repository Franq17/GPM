# -*- coding: utf-8 -*-

import os

from flask_script import Manager

from webapp import create_app
from webapp.extensions import db
from webapp.modelos import User, Rol, Permiso, Proyecto, INICIADO, Comite, Atributo, ACTIVE


app = create_app()
manager = Manager(app)
project_root_path = os.path.join(os.path.dirname(app.root_path))
NINGUNO=0

NO_ASIGNADO=0
ASIGNADO=1

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
    permiso24 = Permiso(nombre=u'modificarFases',descripcion=u'permite modificar Fases')
    permiso25 = Permiso(nombre=u'eliminarFases',descripcion=u'permite eliminar Fases')
    permiso26 = Permiso(nombre=u'verFases',descripcion=u'permite ver Fases')
    
    #*******************Permisos de Lineas Bases*****************************
    permiso27 = Permiso(nombre=u'crearLineaBase',descripcion=u'permite crear Linea Base')
    permiso28 = Permiso(nombre=u'modificarLineaBase',descripcion=u'permite modificar Linea Base')
    permiso29 = Permiso(nombre=u'eliminarLineaBase',descripcion=u'permite eliminar Linea Base')
    permiso30 = Permiso(nombre=u'verLineaBase',descripcion=u'permite ver Linea Base')
    
    #*******************Permisos para control de Usuarios**************************
    permiso31 = Permiso(nombre=u'administrador',descripcion=u'permite verificar si el usuario posee rol de tipo administrador')
    permiso32 = Permiso(nombre=u'liderProyecto',descripcion=u'permite verificar si el usuario posee rol de tipo liderProyecto')
    permiso33 = Permiso(nombre=u'liderFase',descripcion=u'permite verificar si el usuario posee rol de tipo liderFase')
    permiso34 = Permiso(nombre=u'desarrollador',descripcion=u'permite verificar si el usuario posee rol de tipo desarrollador')
    
    db.session.add(permiso1)
    db.session.add(permiso2)
    db.session.add(permiso3)
    db.session.add(permiso4)
    db.session.add(permiso5)
    db.session.add(permiso6)
    db.session.add(permiso7)
    db.session.add(permiso8)
    db.session.add(permiso9)
    db.session.add(permiso10)
    db.session.add(permiso11)
    db.session.add(permiso12)
    db.session.add(permiso13)
    db.session.add(permiso14)
    db.session.add(permiso15)
    db.session.add(permiso16)
    db.session.add(permiso17)
    db.session.add(permiso18)
    db.session.add(permiso19)
    db.session.add(permiso20)
    db.session.add(permiso21)
    db.session.add(permiso22)
    db.session.add(permiso23)
    db.session.add(permiso24)
    db.session.add(permiso25)
    db.session.add(permiso26)
    db.session.add(permiso27)
    db.session.add(permiso28)
    db.session.add(permiso29)
    db.session.add(permiso30)
    db.session.add(permiso31)
    db.session.add(permiso32)
    db.session.add(permiso33)
    db.session.add(permiso34)
    
    rol_admin = Rol(nombre=u'administrador',
                    descripcion=u'rol del administrador',
                    tipo=NINGUNO,
                    estado_id=ASIGNADO,
                    permisoPorRol=[permiso1,permiso2,permiso3,permiso4,permiso5,
                                   permiso6,permiso7,permiso8,permiso9,permiso10,
                                   permiso11,permiso12,permiso13,permiso14,permiso15,
                                   permiso16,permiso17,permiso18,permiso19,permiso20,
                                   permiso21,permiso22,permiso23,permiso24,permiso25,
                                   permiso26,permiso27,permiso28,permiso29,permiso30,
                                   permiso31])
    
    rol_admin_usuarios = Rol(nombre=u'administrador Usuarios',
                    descripcion=u'rol que solo administra usuarios',
                    tipo=NINGUNO,
                    estado_id=ASIGNADO,
                    permisoPorRol=[permiso1,permiso2,permiso3,permiso4])
    
    rol_admin_comites = Rol(nombre=u'administrador Comites',
                    descripcion=u'rol que solo administra comites',
                    tipo=NINGUNO,
                    estado_id=ASIGNADO,
                    permisoPorRol=[permiso14,permiso15,permiso16,permiso17,permiso18])
    
    rol_liderProyecto = Rol(nombre=u'lider de Proyecto',
                    descripcion=u'rol con permisos de lider de Proyecto',
                    tipo=2,
                    estado_id=1,
                    permisoPorRol=[permiso10,permiso11,permiso12,permiso13,permiso14,
                                   permiso15,permiso16,permiso17,permiso18,permiso23,
                                   permiso23,permiso25,permiso26,permiso32])
    
    rol_liderFase = Rol(nombre=u'lider de Fase',
                    descripcion=u'rol con permisos de lider de Fase',
                    tipo=3,
                    estado_id=1,
                    permisoPorRol=[permiso19,permiso20,permiso21,permiso22,permiso26,
                                   permiso27,permiso28,permiso29,permiso30,permiso33])
    
    rol_desarrollador = Rol(nombre=u'desarrollador',
                    descripcion=u'rol con permisos de desarrollador',
                    tipo=4,
                    estado_id=1,
                    permisoPorRol=[permiso19,permiso20,permiso21,permiso22,permiso23,
                                   permiso26,permiso27,permiso28,permiso29,permiso30,
                                   permiso34])
    
    rol_lider = Rol(nombre=u'lider',tipo=NINGUNO, estado_id=NO_ASIGNADO, descripcion=u'rol del lider')
    rol_usuario = Rol(nombre=u'usuario',tipo=NINGUNO, estado_id=NO_ASIGNADO, descripcion=u'rol del usuario')
    
    
    admin = User(
            name=u'admin',
            nombre=u'Adolfo',
            apellido=u'Salas', 
            email=u'admin@example.com', 
            password=u'123456',
            rolPorUsuario=[rol_admin], 
            status_id=ACTIVE
            )
    
    lider = User(
            name=u'lider',
            nombre=u'Francisco',
            apellido=u'Quiñonez',
            email=u'lider@example.com', 
            password=u'123456',
            rolPorUsuario=[rol_admin_usuarios, rol_liderProyecto], 
            status_id=ACTIVE
            )
            
    usuario = User(
            name=u'usuario',
            nombre=u'Pablo',
            apellido=u'Sanchez', 
            email=u'usuario@example.com', 
            password=u'123456',
            rolPorUsuario=[rol_admin_comites, rol_liderFase], 
            status_id=ACTIVE
            )
    
    chino = User(
            name=u'chino',
            nombre=u'Mauro',
            apellido=u'Vera', 
            email=u'chino@example.com', 
            password=u'123456',
            rolPorUsuario=[rol_desarrollador], 
            status_id=ACTIVE
            )
    
    atributoString = Atributo(nombre=u'String',tipo=u'1')
    atributoInt = Atributo(nombre=u'Int',tipo=u'2')
    atributoFecha = Atributo(nombre=u'Fecha',tipo=u'3')
    
    db.session.add(atributoString)
    db.session.add(atributoInt)
    db.session.add(atributoFecha)
    
    db.session.add(admin)
    db.session.add(lider) 
    db.session.add(usuario)
    db.session.add(chino)
    
    db.session.add(rol_admin)
    db.session.add(rol_lider)
    db.session.add(rol_usuario)
    db.session.add(rol_liderProyecto)
    db.session.add(rol_liderFase)
    db.session.add(rol_desarrollador)

    db.session.add(rol_admin_usuarios)
    db.session.add(rol_admin_comites)
    
    

    db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()

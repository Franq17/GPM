# -*- coding: utf-8 -*-

import unittest
#from webapp.extensions import db
from webapp.modelos.models_adm import User, Permiso, Rol, Proyecto, Comite, Fase, Solicitud
from webapp.modelos.models_adm import TipoItem, Item, Atributo, LineaBase, Archivo

class TestUser (unittest.TestCase):
    """Unit test case for the ``User`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.userTest = User(
            name="usuario",
            _password='123456',
            nombre="Pablo",
            apellido="Sanchez",
            telefono="021-123-321",
            ci = 123456,
            email="pablo@email.com",
            status_id=0,
            )
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.userTest
        
    def _makeOne(self, nombre= 'Usertest', email= 'usertest@email.com'):
        user = User(name= nombre, email= email)
        return user
 
    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.name, 'Usertest')
        self.assertEqual(instance.email, 'usertest@email.com')
        print 'Prueba de crear Usuario: Ok'
    
    def test_getPassword(self):
        result = self.userTest._get_password()
        self.assertEqual(result, '123456')
        print 'Prueba de obtencion del password del Usuario: Ok'
      
    def test_getNombreUsuario(self):
        result = self.userTest.getNombreUsuario()
        self.assertEqual(result, 'usuario')
        print 'Prueba de obtencion del nick del Usuario: Ok'
    
    def test_getNombre(self):
        result = self.userTest.getNombre()
        self.assertEqual(result, 'Pablo')
        print 'Prueba de obtencion del Nombre del Usuario: Ok'
    
    def test_getApellido(self):
        result = self.userTest.getApellido()
        self.assertEqual(result, 'Sanchez')
        print 'Prueba de obtencion del Apellido del Usuario: Ok'
    
    def test_getEmail(self):
        result = self.userTest.getEmail()
        self.assertEqual(result, 'pablo@email.com')
        print 'Prueba de obtencion del email del Usuario: Ok'
    
    def test_getTelefono(self):
        result = self.userTest.getTelefono()
        self.assertEqual(result, '021-123-321')
        print 'Prueba de obtencion del telefono del Usuario: Ok'
    
    def test_getCI(self):
        result = self.userTest.getCI()
        self.assertEqual(result, 123456)
        print 'Prueba de obtencion del CI del Usuario: Ok'
    
    def test_getStatus(self):
        result = self.userTest.getStatus()
        self.assertEqual(result, 'inactivo')
        print 'Prueba de obtencion de estado actual del Usuario: Ok'
    
    def test_setNombreUsuario(self):
        self.userTest.setNombreUsuario('admin')
        result = self.userTest.getNombreUsuario()
        self.assertEqual(result, 'admin')
        print 'Prueba de cambio del nick del Usuario: Ok'
    
    def test_setNombre(self):
        self.userTest.setNombre('Rene')
        result = self.userTest.getNombre()
        self.assertEqual(result, 'Rene')
        print 'Prueba de cambio del nombre del Usuario: Ok'
    
    def test_setApellido(self):
        self.userTest.setApellido('Vera')
        result = self.userTest.getApellido()
        self.assertEqual(result, 'Vera')
        print 'Prueba de cambio del apellido del Usuario: Ok'
    
    def test_setEmail(self):
        self.userTest.setEmail('psanz@example.com')
        result = self.userTest.getEmail()
        self.assertEqual(result, 'psanz@example.com')
        print 'Prueba de cambio del email del Usuario: Ok'
        
    def test_setTelefono(self):
        self.userTest.setTelefono('0981123456')
        result = self.userTest.getTelefono()
        self.assertEqual(result, '0981123456')
        print 'Prueba de cambio del telefono del Usuario: Ok'
    
    def test_setCI(self):
        self.userTest.setTelefono('3.111.222')
        result = self.userTest.getTelefono()
        self.assertEqual(result, '3.111.222')
        print 'Prueba de cambio del CI del Usuario: Ok'
    
    def test_setStatus(self):
        self.userTest.setStatus(1)
        result = self.userTest.getStatus()
        self.assertEqual(result, 'activo')
        print 'Prueba de cambio del estado del Usuario: Ok'

class TestPermiso (unittest.TestCase):
    """Unit test case for the ``Permiso`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.permisoTest = Permiso(
            nombre="ver",
            descripcion="permiso de visualizacion",
            )
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.permisoTest
        
    def _makeOne(self, nombre= 'Permiso', descripcion= 'Description'):
        permiso = Permiso(nombre= nombre, descripcion= descripcion)
        return permiso

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'Permiso')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de agregar Permiso: Ok'
    
    def test_getNombre(self):
        result = self.permisoTest.getNombre()
        self.assertEqual(result, 'ver')
        print 'Prueba de obtencion del Nombre del Permiso: Ok'
        
    def test_getDescripcion(self):
        result = self.permisoTest.getDescripcion()
        self.assertEqual(result, 'permiso de visualizacion')
        print 'Prueba de obtencion de la descripcion del Permiso: Ok'
    
    def test_setNombre(self):
        self.permisoTest.setNombre('editar')
        result = self.permisoTest.getNombre()
        self.assertEqual(result, 'editar')
        print 'Prueba de cambio del Nombre del Permiso: Ok'
        
    def test_setDescripcion(self):
        self.permisoTest.setDescripcion('permiso de edicion')
        result = self.permisoTest.getDescripcion()
        self.assertEqual(result, 'permiso de edicion')
        print 'Prueba de cambio de la descripcion del Permiso: Ok'

class TestRol (unittest.TestCase):
    """Unit test case for the ``Rol`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.rolTest = Rol(
            nombre="rol_lider",
            tipo=2, #tipo lider de proyecto (constants)
            descripcion="rol de prueba",
            estado_id=1,
            )
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.rolTest
        
    def _makeOne(self, nombre= 'Role', descripcion= 'Description'):
        role = Rol(nombre= nombre, descripcion= descripcion)
        return role

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'Role')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de agregar Rol: Ok'
    
    def test_getNombre(self):
        result = self.rolTest.getNombre()
        self.assertEqual(result, 'rol_lider')
        print 'Prueba de obtencion del Nombre del Rol: Ok'
    
    def test_getTipo(self):
        result = self.rolTest.getTipo()
        self.assertEqual(result, 'lider de Proyecto')
        print 'Prueba de obtencion del tipo del Rol: Ok'
    
    def test_getDescripcion(self):
        result = self.rolTest.getDescripcion()
        self.assertEqual(result, 'rol de prueba')
        print 'Prueba de obtencion de la descripcion del Rol: Ok'
    
    def test_getEstado(self):
        result = self.rolTest.getEstado()
        self.assertEqual(result, 'asignado')
        print 'Prueba de obtencion de la descripcion del Rol: Ok'
    
    def test_setNombre(self):
        self.rolTest.setNombre('rol_lider_Proyecto')
        result = self.rolTest.getNombre()
        self.assertEqual(result, 'rol_lider_Proyecto')
        print 'Prueba de cambio del Nombre del Rol: Ok'
    
    def test_setTipo(self):
        self.rolTest.setTipo(3)
        result = self.rolTest.getTipo()
        self.assertEqual(result, 'lider de Fase')
        print 'Prueba de cambio del tipo del Rol: Ok'
    
    def test_setDescripcion(self):
        self.rolTest.setDescripcion('rol de tipo lider de fase')
        result = self.rolTest.getDescripcion()
        self.assertEqual(result, 'rol de tipo lider de fase')
        print 'Prueba de cambio de la descripcion del Rol: Ok'
    
    def test_setEstado(self):
        self.rolTest.setEstado(0)
        result = self.rolTest.getEstado()
        self.assertEqual(result, 'no asignado')
        print 'Prueba de cambio del estado del Rol: Ok'

class TestProyecto (unittest.TestCase):
    """Unit test case for the ``Proyecto`` model."""
    
    def setUp (self):
        unittest.TestCase.setUp(self)
        self.proyectoTest = Proyecto(
            nombre='GPM-Systems',
            descripcion='proyecto de desarrollo de SW',
            complejidad_total=10,
            lider_proyecto=1,
            numero_fases=3,
            estado_id = 0,
            )
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.proyectoTest
    
    def _makeOne(self, nombre= 'GPM', descripcion= 'Gestor', complejidad= 10,
                 lider= 1, numero= 3, estado= 0):
        proyecto = Proyecto(nombre= nombre, descripcion= descripcion,
                            complejidad_total= complejidad, lider_proyecto= lider,
                            estado_id= estado)
        return proyecto
 
    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'GPM')
        self.assertEqual(instance.descripcion, 'Gestor')
        print 'Prueba de crear Proyecto: Ok'
    
    def test_getNombre(self):
        result = self.proyectoTest.getNombre()
        self.assertEqual(result, 'GPM-Systems')
        print 'Prueba de obtencion del Nombre del Proyecto: Ok'
    
    def test_getDescripcion(self):
        result = self.proyectoTest.getDescripcion()
        self.assertEqual(result, 'proyecto de desarrollo de SW')
        print 'Prueba de obtencion de la descripcion del Proyecto: Ok'
    
    def test_getComplejidad(self):
        result = self.proyectoTest.getComplejidad()
        self.assertEqual(result, 10)
        print 'Prueba de obtencion de la complejidad total del Proyecto: Ok'
    
    def test_getNroFases(self):
        result = self.proyectoTest.getNroFases()
        self.assertEqual(result, 3)
        print 'Prueba de obtencion de la cantidad de fases del Proyecto: Ok'
    
    def test_getEstado(self):
        result = self.proyectoTest.getEstado()
        self.assertEqual(result, 'no iniciado')
        print 'Prueba de estado inicial del Proyecto: Ok'
    
    def test_setNombre(self):
        self.proyectoTest.setNombre('GPM')
        result = self.proyectoTest.getNombre()
        self.assertEqual(result, 'GPM')
        print 'Prueba de obtencion del Nombre del Proyecto: Ok'
    
    def test_setDescripcion(self):
        self.proyectoTest.setDescripcion('proyecto de desarrollo de software')
        result = self.proyectoTest.getDescripcion()
        self.assertEqual(result, 'proyecto de desarrollo de software')
        print 'Prueba de obtencion de la descripcion del Proyecto: Ok'
    
    def test_setComplejidad(self):
        self.proyectoTest.setComplejidad(20)
        result = self.proyectoTest.getComplejidad()
        self.assertEqual(result, 20)
        print 'Prueba de cambio de la complejidad total del Proyecto: Ok'
    
    def test_setEstado(self):
        self.proyectoTest.setEstado(2)
        result = self.proyectoTest.getEstado()
        self.assertEqual(result, 'finalizado')
        print 'Prueba cambio de estado del Proyecto: Ok'
    
class TestComite (unittest.TestCase):
    """Unit test case for the ``Comite`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.comite = Comite()
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.comite
        
    def _makeOne(self, nombre= 'ComiteTest', descripcion= 'Description'):
        comite = Comite(nombre= nombre, descripcion= descripcion)
        return comite

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'ComiteTest')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de crear Comite: Ok'

class TestFase(unittest.TestCase):
    """Unit test case for the ``Fase`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.userTest = User(
            id=1,
            name="usuario",
            _password='123456',
            nombre="Pablo",
            apellido="Sanchez",
            telefono="021-123-321",
            ci = 123456,
            email="pablo@email.com",
            status_id=0,
            )
        
        self.tipoItem = TipoItem(
            nombre='tipo',
            descripcion='descripcion',
            proyecto_id=1,
            )
        
        self.item1 = Item(
            nombre='item1',
            descripcion='descripcion',
            version=1,
            complejidad=4,
            estado_id=0,
            )
        
        self.item2 = Item(
            nombre='item2',
            descripcion='descripcion',
            version=1,
            complejidad=3,
            estado_id=0,
            )
        
        self.faseTest = Fase(
            nombre='Analisis',
            descripcion='Fase de Analisis del proyecto de desarrollo de SW',
            numero_fase=1,
            numero_lb=1,
            estado_id=0,
            items=[self.item1, self.item2],
            tipoItemPorFase=[self.tipoItem],
            )
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.faseTest, self.item1, self.item2, self.tipoItem, self.userTest
        
    def _makeOne(self, nombre= 'FaseTest', descripcion= 'Description'):
        fase = Fase(nombre= nombre, descripcion= descripcion)
        return fase

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'FaseTest')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de agregar Fase: Ok'
    
    def test_getNombre(self):
        result = self.faseTest.getNombre()
        self.assertEqual(result, 'Analisis')
        print 'Prueba de obtencion del Nombre de Fase: Ok'
    
    def test_getDescripcion(self):
        result = self.faseTest.getDescripcion()
        self.assertEqual(result, 'Fase de Analisis del proyecto de desarrollo de SW')
        print 'Prueba de obtencion de la descripcion de una Fase: Ok'
    
    def test_getNroFase(self):
        result = self.faseTest.getNroFase()
        self.assertEqual(result, 1)
        print 'Prueba de obtencion del numero fase del Proyecto: Ok'
      
    def test_getNroLB(self):
        result = self.faseTest.getNroLB()
        self.assertEqual(result, 1)
        print 'Prueba de obtencion de la cantidad de LB de una fase del Proyecto: Ok'
  
#     def test_getItems(self):
#         result = self.faseTest.getItems()
#         self.assertEqual(result[0], self.item1)
#         self.assertEqual(result[1], self.item2)
#         print 'Prueba de obtencion de items del Proyecto: Ok'
    
    def test_getNroItems(self):
        result = self.faseTest.getNroItems()
        self.assertEqual(result, 2)
        print 'Prueba de obtencion de la cantidad de items del Proyecto: Ok'
    
    def test_getEstado(self):
        result = self.faseTest.getEstado()
        self.assertEqual(result, 'inicial')
        print 'Prueba de obtencion del estado de una fase del Proyecto: Ok'
    
    def test_existeTipoItem(self):
        self.assertTrue(self.faseTest.existeTipoItem(self.tipoItem.id))
        print 'Prueba de comprobacion de existencia de un tipo de item de una fase: Ok'
    
    def test_setNombre(self):
        self.faseTest.setNombre('Diseño')
        result = self.faseTest.getNombre()
        self.assertEqual(result, 'Diseño')
        print 'Prueba de cambio del Nombre de Fase: Ok'
    
    def test_setDescripcion(self):
        self.faseTest.setDescripcion('Fase de Diseño del proyecto de desarrollo de SW')
        result = self.faseTest.getDescripcion()
        self.assertEqual(result, 'Fase de Diseño del proyecto de desarrollo de SW')
        print 'Prueba de cambio de la descripcion de una Fase: Ok'
        
    def test_setNroLB(self):
        self.faseTest.setNroLB(3)
        result = self.faseTest.getNroLB()
        self.assertEqual(result, 3)
        print 'Prueba de cambio de la cantidad de LB del Proyecto: Ok'
 
    def test_setEstado(self):
        self.faseTest.setEstado(3)
        result = self.faseTest.getEstado()
        self.assertEqual(result, 'comprometida')
        print 'Prueba de cambio del estado de una fase del Proyecto: Ok'
    
    def test_setLider(self):
        self.faseTest.setLider(self.userTest.id)
        self.assertEqual(self.faseTest.lider_fase, 1)
        print 'Prueba de cambio de lider de una fase del Proyecto: Ok'

class TestTipoItem(unittest.TestCase):
    """Unit test case for the ``Tipo de Item`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.tipoItemTest = TipoItem(
            nombre='tipo',
            descripcion='descripcion',
            proyecto_id=1,
            )
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.tipoItemTest
        
    def _makeOne(self, nombre= 'TipoItemTest', descripcion= 'Description'):
        tipoItem = TipoItem(nombre= nombre, descripcion= descripcion)
        return tipoItem

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'TipoItemTest')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de crear Tipo de Item: Ok'
    
    def test_getNombre(self):
        result = self.tipoItemTest.getNombre()
        self.assertEqual(result, 'tipo')
        print 'Prueba de obtencion del Nombre del tipo de Item: Ok'
    
    def test_getDescripcion(self):
        result = self.tipoItemTest.getDescripcion()
        self.assertEqual(result, 'descripcion')
        print 'Prueba de obtencion de la descripcion del tipo de Item: Ok'
    
    def test_setNombre(self):
        self.tipoItemTest.setNombre('tipoItem')
        result = self.tipoItemTest.getNombre()
        self.assertEqual(result, 'tipoItem')
        print 'Prueba de cambio del Nombre del tipo de Item: Ok'
    
    def test_setDescripcion(self):
        self.tipoItemTest.setDescripcion('ejemplo de tipo de item')
        result = self.tipoItemTest.getDescripcion()
        self.assertEqual(result, 'ejemplo de tipo de item')
        print 'Prueba de cambio de la descripcion del tipo de Item: Ok'

class TestItem(unittest.TestCase):
    """Unit test case for the ``Item`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.itemTest = Item(
            nombre='item',
            descripcion='descripcion',
            version=1,
            complejidad=4,
            estado_id=0,
            lineaBase_id=1,
            marcado='No'
            )
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.itemTest
        
    def _makeOne(self, nombre= 'ItemTest', descripcion= 'Description'):
        item = Item(nombre= nombre, descripcion= descripcion)
        return item

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'ItemTest')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de crear Item: Ok'
    
    def test_getNombre(self):
        result = self.itemTest.getNombre()
        self.assertEqual(result, 'item')
        print 'Prueba de obtencion del Nombre del Item: Ok'
    
    def test_getDescripcion(self):
        result = self.itemTest.getDescripcion()
        self.assertEqual(result, 'descripcion')
        print 'Prueba de obtencion de la descripcion del Item: Ok'
    
    def test_getVersion(self):
        result = self.itemTest.getVersion()
        self.assertEqual(result, 1)
        print 'Prueba de obtencion de la version del Item: Ok'
        
    def test_getComplejidad(self):
        result = self.itemTest.getComplejidad()
        self.assertEqual(result, 4)
        print 'Prueba de obtencion de la complejidad del Item: Ok'
    
    def test_getEstado(self):
        result = self.itemTest.getEstado()
        self.assertEqual(result, 'desaprobado')
        print 'Prueba de obtencion del estado del Item: Ok'
    
    def test_setNombre(self):
        self.itemTest.setNombre('itemTest')
        result = self.itemTest.getNombre()
        self.assertEqual(result, 'itemTest')
        print 'Prueba de cambio del Nombre del Item: Ok'
    
    def test_setDescripcion(self):
        self.itemTest.setDescripcion('ejemplo')
        result = self.itemTest.getDescripcion()
        self.assertEqual(result, 'ejemplo')
        print 'Prueba de cambio de la descripcion del Item: Ok'
    
    def test_setVersion(self):
        self.itemTest.setVersion(3)
        result = self.itemTest.getVersion()
        self.assertEqual(result, 3)
        print 'Prueba de cambio de la version del Item: Ok'
        
    def test_setComplejidad(self):
        self.itemTest.setComplejidad(7)
        result = self.itemTest.getComplejidad()
        self.assertEqual(result, 7)
        print 'Prueba de cambio de la complejidad del Item: Ok'
    
    def test_setEstado(self):
        self.itemTest.setEstado(3)
        result = self.itemTest.getEstado()
        self.assertEqual(result, 'bloqueado')
        print 'Prueba de obtencion del estado del Item: Ok'
        
    def test_tieneLineaBase(self):
        self.assertTrue(self.itemTest.tieneLineaBase())
        print 'Prueba de comprobacion de si el item esta en una LB: Ok'
        
    def test_marcarRevision(self):
        self.itemTest.marcarRevision()
        result = self.itemTest.getEstado()
        self.assertEqual(result, 'revision')
        print 'Prueba de marcacion de revision de el item: Ok'

    def test_getMarcado(self):
        result = self.itemTest.getMarcado()
        self.assertEqual(result, 'No')
        print 'Prueba de obtencion del marcado del Item: Ok'

    def test_setMarcar(self):
        self.itemTest.setMarcar()
        self.assertEqual(self.itemTest.getMarcado(),'Si')
        print 'Prueba de marcado del item: Ok'

    def test_setDesMarcar(self):
        self.itemTest.setMarcar()
        self.itemTest.setDesMarcar()
        self.assertEqual(self.itemTest.getMarcado(),'No')
        print 'Prueba de desmarcado del item: Ok'

class TestAtributo(unittest.TestCase):
    """Unit test case for the ``Atributo`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.atributo = Atributo()
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.atributo
        
    def _makeOne(self, nombre= 'AtributoTest', descripcion= 'Description'):
        atributo = Atributo(nombre= nombre, descripcion= descripcion)
        return atributo

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'AtributoTest')
        #self.assertEqual(intance.tipo, string)
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de crear Atributo: Ok'

class TestArchivo(unittest.TestCase):
    """Unit test case for the ``Archivo`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.archivoTest = Archivo(
            valor= 'RjO6p3LZ1S',
            tipoArchivo= 'jpg',
            nombreArchivo= 'imagen10',
            )
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.archivoTest
        
    def _makeOne(self, valor= 'asdf1234',
                 tipo= 123456, nombre= 'imagen'):
        archivo = Archivo(valor= valor, tipoArchivo= tipo, nombreArchivo= nombre)
        return archivo

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.valor, 'asdf1234')
        self.assertEqual(instance.tipoArchivo, 123456)
        self.assertEqual(instance.nombreArchivo, 'imagen')
        print 'Prueba de crear Atributo: Ok'
    
    def test_getArchivo(self):
        result = self.archivoTest.getArchivo()
        self.assertEqual(result, 'RjO6p3LZ1S')
        print 'Prueba de obtener el valor del archivo externo: Ok'
    
    def test_getTipoArchivo(self):
        result = self.archivoTest.getTipoArchivo()
        self.assertEqual(result, 'jpg')
        print 'Prueba de obtener el tipo de archivo externo: Ok'
    
    def test_getNombreArchivo(self):
        result = self.archivoTest.getNombreArchivo()
        self.assertEqual(result, 'imagen10')
        print 'Prueba de obtener el nombre archivo externo: Ok'
    
    def test_setArchivo(self):
        self.archivoTest.setArchivo('Psanz10')
        result = self.archivoTest.getArchivo()
        self.assertEqual(result, 'Psanz10')
        print 'Prueba de cambio de archivo externo: Ok'
    
    def test_setTipoArchivo(self):
        self.archivoTest.setTipoArchivo(654321)
        result = self.archivoTest.getTipoArchivo()
        self.assertEqual(result, 654321)
        print 'Prueba de obtener archivo externo: Ok'
    
    def test_setNombreArchivo(self):
        self.archivoTest.setNombreArchivo('documento')
        result = self.archivoTest.getNombreArchivo()
        self.assertEqual(result, 'documento')
        print 'Prueba de edicion del nombre archivo externo: Ok'

class TestLineaBase(unittest.TestCase):
    """Unit test case for the ``Linea Base`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.item1 = Item(
            nombre='item1',
            descripcion='descripcion',
            version=1,
            complejidad=4,
            estado_id=0,
            )
        
        self.item2 = Item(
            nombre='item2',
            descripcion='descripcion',
            version=1,
            complejidad=3,
            estado_id=0,
            )
        
        self.lineaBase = LineaBase()
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.lineaBase
        
    def _makeOne(self, numero= 3, nombre= 'LBtest', estado= 0, complejidad= 0):
        lineaBase = LineaBase(numero_lb= numero, nombre= nombre,
                              estado_id= estado, complejidad= complejidad)
        return lineaBase

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.numero_lb, 3)
        self.assertEqual(instance.nombre, 'LBtest')
        self.assertEqual(instance.estado_id, 0)
        self.assertEqual(instance.complejidad, 0)
        print 'Prueba de crear Linea Base: Ok'
 
class TestSolicitud (unittest.TestCase):
    """Unit test case for the ``Solicitud`` model."""
     
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.solicitud = Solicitud(
            estado=0,
            voto=0,
            solicitante=1,
            )
      
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.solicitud
         
    def _makeOne(self, estado=0, voto=0, solicitante_id=1):
        solicitud = Solicitud(estado=estado, voto=voto, solicitante=solicitante_id)
        return solicitud
 
    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.estado, 0)
        self.assertEqual(instance.voto, 0)
        self.assertEqual(instance.solicitante, 1)
        print 'Prueba de crear Comite: Ok'
    
    def test_getEstado(self):
        result = self.solicitud.getEstado()
        self.assertEqual(result, 'no votado')
        print 'Prueba de obtencion del estado de la solicitud: Ok'
    
    def test_getVoto(self):
        result = self.solicitud.getVoto()
        self.assertEqual(result, 'no votado')
        print 'Prueba de obtencion del voto de la solicitud: Ok'
    
    def test_getSolicitante(self):
        result = self.solicitud.getSolicitante()
        self.assertEqual(result, 1)
        print 'Prueba de obtencion del solicitante de la solicitud: Ok'
    
    def test_setEstado(self):
        self.solicitud.setEstado(2)
        result = self.solicitud.getEstado()
        self.assertEqual(result, 'finalizado')
        print 'Prueba de cambio del estado de la solicitud: Ok'
    
    def test_setVoto(self):
        self.solicitud.setVoto(2)
        result = self.solicitud.getVoto()
        self.assertEqual(result, 'rechazado')
        print 'Prueba de seteo del voto de la solicitud: Ok'
    
    def test_setSolicitante(self):
        self.solicitud.setSolicitante(2)
        result = self.solicitud.getSolicitante()
        self.assertEqual(result, 2)
        print 'Prueba de seteo del solicitante de la solicitud: Ok'

if __name__ == "__main__":
    unittest.main() # run all tests

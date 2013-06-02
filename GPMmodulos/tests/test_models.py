# -*- coding: utf-8 -*-

import unittest
#from webapp.extensions import db
from webapp.modelos.models_adm import User, Permiso, Rol, Proyecto, Comite, Fase
from webapp.modelos.models_adm import TipoItem, Item, Atributo, LineaBase

class TestUser (unittest.TestCase):
    """Unit test case for the ``User`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.userTest = User(
            name="pablo",
            _password='123456',
            nombre="Pablo",
            apellido="Sanchez",
            telefono="021-123-321",
            ci = 123456,
            email="pablo@email.com",
            role_id=0,
            status_id=0,
            #rolPorUsuario=[self.rolTest]
            )
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.userTest

    def test_getRole(self):
        result = self.userTest.getRole()
        self.assertEqual(result, 'admin')
        print 'Prueba de obtencion de rol: Ok'
        
    def test_IsAdmin(self):
        result = self.userTest.is_admin()
        self.assertEqual(result, 1)
        print 'Prueba de si es un usuario admin: Ok'
        
    def test_getStatus(self):
        result = self.userTest.getStatus()
        self.assertEqual(result, 'inactive')
        print 'Prueba de obtencion de estado actual del Usuario: Ok'
    
#     def test_getProyectos(self):
#         result = self.userTest.getProyectos()
#         self.assertEqual(result, 'proyectoDePrueba')
#         print 'Prueba de obtencion de un proyecto asignado a un Usuario: Ok'   
        
#     def test_comprobarPermiso(self):
#         #rol = self.usertest.getRole()
#         result = self.userTest.comprobarPermiso('ver')
#         self.assertTrue(result)
#         print 'Prueba de comprobacion de permiso de un Usuario: Ok'
        
    def _makeOne(self, nombre= 'Usertest', email= 'usertest@email.com'):
        user = User(name= nombre, email= email)
        return user
 
    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.name, 'Usertest')
        self.assertEqual(instance.email, 'usertest@email.com')
        print 'Prueba de crear Usuario: Ok'

class TestPermiso (unittest.TestCase):
    """Unit test case for the ``Permiso`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.permiso = Permiso()
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.permiso
        
    def _makeOne(self, nombre= 'Permiso', descripcion= 'Description'):
        permiso = Permiso(nombre= nombre, descripcion= descripcion)
        return permiso

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'Permiso')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de agregar Permiso: Ok'

class TestRol (unittest.TestCase):
    """Unit test case for the ``Rol`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.rol = Rol()
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.rol
        
    def _makeOne(self, nombre= 'Role', descripcion= 'Description'):
        role = Rol(nombre= nombre, descripcion= descripcion)
        return role

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'Role')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de agregar Rol: Ok'

class TestProyecto (unittest.TestCase):
    """Unit test case for the ``Proyecto`` model."""
    
    def setUp (self):
        unittest.TestCase.setUp(self)
        self.proyectotest = Proyecto(
            nombre='proyectoPrueba',
            descripcion='descripcion',
            lider_proyecto='',
            numero_fases=3,
            estado_id = 0,
            )
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.proyectotest
        
    def test_getStatus(self):
        result = self.proyectotest.getStatus()
        self.assertEqual(result, 'no iniciado')
        print 'Prueba de estado inicial del Proyecto: Ok'
    
    def _makeOne(self, nombre= 'GPM', descripcion= 'Gestor'):
        proyecto = Proyecto(nombre= nombre, descripcion= descripcion)
        return proyecto
 
    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'GPM')
        self.assertEqual(instance.descripcion, 'Gestor')
        print 'Prueba de crear Proyecto: Ok'
        
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
        self.fase = Fase()
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.fase
        
    def _makeOne(self, nombre= 'FaseTest', descripcion= 'Description'):
        fase = Fase(nombre= nombre, descripcion= descripcion)
        return fase

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'FaseTest')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de agregar Fase: Ok'

class TestTipoItem(unittest.TestCase):
    """Unit test case for the ``Tipo de Item`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.tipoItem = TipoItem()
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.tipoItem
        
    def _makeOne(self, nombre= 'TipoItemTest', descripcion= 'Description'):
        tipoItem = TipoItem(nombre= nombre, descripcion= descripcion)
        return tipoItem

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'TipoItemTest')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de crear Tipo de Item: Ok'

class TestItem(unittest.TestCase):
    """Unit test case for the ``Item`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.item = Item()
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.item
        
    def _makeOne(self, nombre= 'ItemTest', descripcion= 'Description'):
        item = Item(nombre= nombre, descripcion= descripcion)
        return item

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.nombre, 'ItemTest')
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de crear Item: Ok'

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

class TestLineaBase(unittest.TestCase):
    """Unit test case for the ``Linea Base`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.lineaBase = LineaBase()
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.lineaBase
        
    def _makeOne(self, numero= 3, descripcion= 'Description'):
        lineaBase = LineaBase(numero_lb= numero, descripcion= descripcion)
        return lineaBase

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.numero_lb, 3)
        self.assertEqual(instance.descripcion, 'Description')
        print 'Prueba de crear Linea Base: Ok'

if __name__ == "__main__":
    unittest.main() # run all tests

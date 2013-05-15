# -*- coding: utf-8 -*-

import unittest
import os

#from webapp.extensions import db
from webapp.modelos.models_adm import User, Rol, Proyecto

basedir = os.path.abspath(os.path.dirname(__file__))

class TestUser (unittest.TestCase):
    """Unit test case for the ``User`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.usertest = User(
            name="pablo",
            _password='123456',
            nombre="Pablo",
            apellido="Sanchez",
            telefono="021-123-321",
            ci = 123456,
            email="pablo@email.com",
            role_id=0 )
#         
#     def testTrue(self):
#         self.usertest = User(
#             name="pablo",
#             _password="123456",
#             nombre="Pablo",
#             apellido="Sanchez",
#             telefono="021-123-321",
#             ci = 123456,
#             email="pablo@email.com")
        
#     def _getTargetClass(self):
#         from webapp.modelos.models_adm import User
#         return User
# 
#     def _makeOne(self,
#                  name= 'nombreUsuario',
#                  _password='password',
#                  nombre='nombre',
#                  apellido='apellido',
#                  telefono=22,
#                  ci=22,
#                  mail='mail@gmail.com'):
#         return self._getTargetClass()(name, _password, nombre, apellido, telefono, ci, mail)
# 
#     def test_constructor(self):
#         instance = self._makeOne()
#         self.assertEqual(instance.name, 'nombreUsuario')
#         self.assertEqual(instance.nombre, 'nombre')
#         self.assertEqual(instance.apellido, 'apellido')
#         self.assertEqual(instance.telefono, 22)
#         self.assertEqual(instance.ci, 22)
#         self.assertEqual(instance.mail, 'mail@gmail.com')
#         print 'Prueba de agregar Usuario: Ok'
        
    def test_authenticate(self):
        result = self.usertest.is_authenticated()
        self.assertTrue(result)
        print 'Prueba de autenticación del usuario: Ok'
    
    def test_checkpassword(self):
        result = self.usertest.check_password('123456')
        self.assertEqual(result, 0)
        print 'Prueba de checkeo de contraseña: Ok'
        
    def test_UserIsAdmin(self):
        result = self.usertest.is_admin()
        self.assertEqual(result, 1)
        print 'Prueba de si es un usuario admin: Ok'


class TestRol (unittest.TestCase):
    """Unit test case for the ``Rol`` model."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.rol = Rol()
     
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.rol
        
#     def testTrue(self):
        

#     def _getTargetClass(self):
#         from webapp.modelos.models_adm import Rol
#         return Rol
# 
#     def _makeOne(self, nombre= 'nombreRol', descripcion='descripcion'):
#         return self._getTargetClass()(nombre, descripcion)
# 
#     def test_constructor(self):
#         instance = self._makeOne()
#         self.assertEqual(instance.nombre, 'nombreRol')
#         print 'Prueba de agregar Rol: Ok'
 
class TestProyecto (unittest.TestCase):
    """Unit test case for the ``Proyecto`` model."""
    
    def setUp (self):
        unittest.TestCase.setUp(self)
        self.proyectotest = Proyecto(
            nombre='proyectoPrueba',
            descripcion='descripcion',
            lider_proyecto='',
            numero_fases=3
            )
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.proyectotest
    
#     def testGetStatus(self):
#         result = self.proyectotest.getStatus()
#         self.assertEquals(result, 0)
#         print 'Prueba de estado inicial del Proyecto: Ok'

if __name__ == "__main__":
    unittest.main() # run all tests
    
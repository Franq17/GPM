# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~

    Define TestCase as base class for unit tests.
    Ref: http://packages.python.org/Flask-Testing/
"""

from flask_testing import TestCase as Base, Twill

from webapp import create_app
from webapp.modelos.models_adm import User
from webapp.modelos.constants import ACTIVE
from webapp.configs import TestConfig
from webapp.extensions import db

class TestCase(Base):
    """Base TestClass for your application."""

    def create_app(self):
        """Create and return a testing flask app."""

        app = create_app(TestConfig)
        self.twill = Twill(app, port=3000)
        return app

    def init_data(self):

        demo = User(name=u'demo', 
            email=u'usuario@example.com', 
            password=u'123456', 
            #role_id=USER,
            status_id=ACTIVE)
#             user_detail=UserDetail(
#                 nameReal=u'Francisco',
# 				apellido=u'quiñonez',
#                 location=u'Hangzhou', 
# 				document=4575,
#                 descripcion=u'usuario is ... hmm ... just a demo guy.'),
#                 )
        admin = User(name=u'admin', 
                email=u'admin@example.com', 
                password=u'123456', 
                #role_id=ADMIN,
                status_id=ACTIVE)
#                 user_detail=UserDetail(
#                     nameReal=u'lorena',
# 					apellido=u'zalazar',
#                 	location=u'Hangzhou', 
# 					document=4575,
#                 	descripcion=u'usuario is ... hmm ... just a demo guy.'),
#                 )

        db.session.add(demo)
        db.session.add(admin)
        db.session.commit()

    def setUp(self):
        """Reset all tables before testing."""

        db.create_all()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""

        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        data = {
            'login': username,
            'password': password,
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        return response

    def _logout(self):
        response = self.client.get('/logout')
        self.assertRedirects(response, location='/')

    def _test_get_request(self, endpoint, template=None):
        response = self.client.get(endpoint)
        self.assert_200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response

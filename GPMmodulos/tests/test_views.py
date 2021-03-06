# -*- coding: utf-8 -*-

from werkzeug.urls import url_quote
from webapp.modelos.models_adm import User, USER_STATUS
from webapp.extensions import db, mail

from tests import TestCase


class TestFrontend(TestCase):

    def test_show(self):
        self._test_get_request('/', 'index.html')

    def test_login(self):
        self._test_get_request('/login', 'frontend/login.html')

    def test_logout(self):
        self.login('demo', '123456')
        self._logout()

    def test_footers(self):
        for page in ['about', 'blog', 'help', 'privacy', 'terms']:
            self._test_get_request('/%s' % page, 'frontend/footers/%s.html' % page)


class TestSearch(TestCase):

    def setUp(self):
        super(TestSearch, self).setUp()
        for i in range(25):
            name = 'user%d' % i
            email = '%s@example.com' % name
            user = User(name=name, email=email, password='123456')
            db.session.add(user)
        db.session.commit()

    def _search(self, keywords, total):
        """
        Since get_context_variable is only inited in setUp(), we have to split
        them into different test_*().
        """
 
        response = self._test_get_request('/search?keywords=%s' % keywords, 'frontend/search.html')
        self.assert200(response)
        self.assertTemplateUsed(name='frontend/search.html')
        pagination = self.get_context_variable('pagination')
        assert pagination.total == total

#    def test_search_name1(self):
#        self._search('user', 25)
#
#    def test_search_name2(self):
#        self._search('user11', 1)
#
#    def test_search_name3(self):
#        self._search('abc', 0)

#    def test_search_email(self):
#        self._search('2@example.com', 3)


#class TestUser(TestCase):
#
#    def test_show(self):
#        username = "demo"
#        self._test_get_request('/user/%s' % username, 'index/show.html')
#
#        self.login('demo', '123456')
#        response = self.client.get('/user/%s' % username)
#        self.assertRedirects(response, location='//')
#
#    def test_home(self):
#        response = self.client.get('/user/')
#        self.assertRedirects(response, location='/login?next=%s' %
#                             url_quote('/user/', safe=''))
#
#        self.login('demo', '123456')
#        self._test_get_request('/user/', 'user/index.html')

class TestSettings(TestCase):

    def test_password(self):
        endpoint = '/settings/password'

        response = self.client.get(endpoint)
        self.assertRedirects(response, location='/login?next=%s' % url_quote(endpoint, safe=''))

        self.login('demo', '123456')
        response = self.client.get('/settings/password')
        self.assert200(response)
        self.assertTemplateUsed("settings/password.html")

        data = {
            'password': '123456',
            'new_password': '654321',
            'password_again': '654321',
        }
        response = self.client.post(endpoint, data=data)
        assert "help-block error" not in response.data
        self.assert200(response)
        self.assertTemplateUsed("settings/password.html")

        updated_user = User.query.filter_by(name='demo').first()
        assert updated_user is not None
        assert updated_user.check_password('654321')


class TestError(TestCase):

    def test_404(self):
        response = self.client.get('/404/')
        self.assert404(response)
        self.assertTemplateUsed('errors/page_not_found.html')

#     def test_403(self):
#         response = self.client.get('/403/')
#         self.assert403(response)
#         self.assertTemplateUsed('errors/forbidden_page.html')
# 
#     def test_500(self):
#         response = self.client.get('/500/')
#         self.assert500(response)
#         self.assertTemplateUsed('errors/server_error.html')




import unittest, os
from flask import current_app
from source import create_app, db
from icecream import ic
from config import TestConfig

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_home_page_redirect(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.request.path == '/'

    def test_registration_form(self):
        response = self.client.get('/auth/register')
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert 'name="username"' in html
        assert 'name="email"' in html
        assert 'name="password"' in html
        assert 'name="confirm"' in html
        assert 'name="submit"' in html
        
    def test_register_user(self):
        response = self.client.post('/auth/register', data={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'foo',
            'confirm': 'foo',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/auth/login'

        print("\nLAST LINE")
import unittest, os
from flask import current_app
from app import create_app, db
from flask_simple_captcha import CAPTCHA
from icecream import ic
from bs4 import BeautifulSoup as bs

# in-memory database, do not provide filename
os.environ['DATABASE_URL'] = 'sqlite:///:memory'

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['DATABASE_URL'] = 'sqlite:///:memory' # this is my own
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory' # also my own
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()
        self.captcha = CAPTCHA({
            'EXPIRE_NORMALIZED': 60
        })

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
        html = response.get_data(as_text=True) # default is byte object, convert it to text

        assert 'name="username"' in html
        assert 'name="email"' in html
        assert 'name="password"' in html
        assert 'name="confirm"' in html
        assert 'name="captcha-hash"' in html
        assert 'name="captcha-text"' in html
        assert 'name="submit"' in html

        # OK

        # CSRF token is disabled for tests that require post request
        # Captcha must also be dispabled or verified
        # for this i will refer to flask-simple-captcha documentation

        # let's just test if without captcha, see what will happen
        # raises 400 Bad request
        # the correct thing to do is to first send a get request, and fetch the captcha hash and captcha text
        # and submit the both along with our post request
        # i assume html page needs to be somehow parsed and captcha elements must be get
        # let's try BeautifulSoup
        
    # def test_captcha_element(self):
        # response = self.client.get('/auth/register')
        # assert response.status_code == 200
        # print("THIS SHOULD PRINT") print statements normally won't print
        # because pytest controls the standard output
        # use '-s' with pytest command, may result in small difficulties
        # html = response.get_data()
        # soup = bs(html, 'html.parser')
        # captcha_hash = soup.find("input", {"name": "captcha-hash"})
        # ic(captcha_hash['value'])
        # captcha_text = soup.find("input", {"name": "captcha-text"})

    def test_register_user(self):
        result = self.captcha.create()
        text = result['text']
        c_hash = result['hash']
        response = self.client.post('/auth/register', data={
            'captcha-hash': c_hash,
            'captcha-text': text,
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'foo',
            'confirm': 'foo',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/auth/login' # redirected to login
        
        print("\nLAST LINE")
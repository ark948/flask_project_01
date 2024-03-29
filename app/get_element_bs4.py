# need a client to get a page
from icecream import ic
import jwt

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()
        self.captcha = CAPTCHA({
            'EXPIRE_NORMALIZED': 60
        })

    def test_captcha_element(self):
        get_response = self.client.get('/auth/register')
        assert get_response.status_code == 200
        # because pytest controls the standard output
        # use '-s' with pytest command, may result in small difficulties
        html = get_response.get_data()
        soup = bs(html, 'html.parser')
        captcha_hash = soup.find("input", {"name": "captcha-hash"})
        ic(captcha_hash['value'])
        captcha_text = soup.find("input", {"name": "captcha-text"})
        ic(type(captcha_hash['value']))
        decoded = jwt.decode(captcha_hash['value'], 'LONG_KEY', algorithms=['HS256'])
        ic(decoded)
        print("\nONLY HASHED TEXT:")
        ic(decoded['hashed_text'])

        # there is no point  in this. even if i could get the token, still would be useless without knowing the captcha text.

        print("\nLAST LINE")
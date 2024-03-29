# need a client to get a page

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
        response = self.client.get('/auth/register')
        assert response.status_code == 200
        # print("THIS SHOULD PRINT") print statements normally won't print
        # because pytest controls the standard output
        # use '-s' with pytest command, may result in small difficulties
        html = response.get_data()
        soup = bs(html, 'html.parser')
        captcha_hash = soup.find("input", {"name": "captcha-hash"})
        # ic(captcha_hash['value'])
        captcha_text = soup.find("input", {"name": "captcha-text"})
        
        print("LAST LINE")
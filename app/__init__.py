from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_simple_captcha import CAPTCHA
from config import CaptchaConfig


db = SQLAlchemy()
migrate = Migrate()
Captcha = CAPTCHA(config=CaptchaConfig)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    Captcha.init_app(app)

    # test route removed by adding main blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
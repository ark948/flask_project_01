from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_simple_captcha import CAPTCHA
from config import CaptchaConfig
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
Captcha = CAPTCHA(config=CaptchaConfig)
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    Captcha.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "برای دسترسی به این صفحه باید وارد سایت شوید."

    # test route removed by adding main blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.error_handler import error_handler_bp
    app.register_blueprint(error_handler_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.shop import bp as shop_bp
    app.register_blueprint(shop_bp, url_prefix='/shop')

    from app.blog import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    return app
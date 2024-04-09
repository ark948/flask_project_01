from flask import Flask
from config import Config
from source.admin import AdminIndexView, HelloView, UserAdminView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_simple_captcha import CAPTCHA
from config import CaptchaConfig
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_ckeditor import CKEditor
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging, os

db = SQLAlchemy()
migrate = Migrate()
Captcha = CAPTCHA(config=CaptchaConfig)
login_manager = LoginManager()
mail = Mail()
admin = Admin(index_view=AdminIndexView())
ckeditor = CKEditor()

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_class)
    app.config['CKEDITOR_SERVE_LOCAL'] = True

    db.init_app(app)
    migrate.init_app(app, db)
    Captcha.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "برای دسترسی به این صفحه باید وارد سایت شوید."
    mail.init_app(app)
    admin.init_app(app)
    ckeditor.init_app(app)

    # admin views
    from source.models.user import User
    admin.add_view(HelloView(name='Hello'))
    admin.add_view(UserAdminView(User, db.session))

    # test route removed by adding main blueprint
    from source.main import bp as main_bp
    app.register_blueprint(main_bp)

    from source.error_handler import error_handler_bp
    app.register_blueprint(error_handler_bp)

    from source.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from source.shop import bp as shop_bp
    app.register_blueprint(shop_bp, url_prefix='/shop')

    from source.blog import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    # SMTPHandler for app.logger
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_SERVER'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='flask_app_failure',
                credentials=auth, secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=10240, backupCount=0)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask_app startup')

    return app
from flask import Flask
# import configuration file
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # test route removed by adding main blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
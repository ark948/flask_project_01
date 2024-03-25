from flask import Flask
# import configuration file
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # test route removed by adding main blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
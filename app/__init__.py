from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate=Migrate()

def create_app(script_info=None):
    app = Flask(__name__)
    
    config_name= os.environ.get('CONFIGURATION')
    app.config.from_object(config['default'])

    db.init_app(app)
    CORS(app)
    migrate.init_app(app,db)

    # registering blueprints
    from app.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

     # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app

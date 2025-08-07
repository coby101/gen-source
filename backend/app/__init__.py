import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app():
    app = Flask(__name__)

    # Choose config class based on FLASK_ENV
    env = os.getenv("FLASK_ENV", "production")

    if env == "development":
        from app.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif env == "testing":
        from app.config import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        from app.config import Config
        app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

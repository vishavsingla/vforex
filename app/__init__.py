from flask import Flask
import logging
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .api import api_blueprint
    app.register_blueprint(api_blueprint)

    from .scheduler import start_scheduler
    start_scheduler()

    return app

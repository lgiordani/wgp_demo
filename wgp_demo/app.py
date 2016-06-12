# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_cors import CORS

from wgp_demo.settings import DevConfig, ProdConfig
from wgp_demo.rest import artists


def create_app(config_object=DevConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/"""
    app = Flask(__name__)
    app.config.from_object(config_object)
    CORS(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(artists.blueprint)
    return None


def create_and_initialize_app():
    CONFIG = ProdConfig if os.environ.get('WGP_DEMO_ENV') == 'prod' else DevConfig
    _app = create_app(CONFIG)
    return _app

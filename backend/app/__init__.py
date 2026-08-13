import os

from dotenv import load_dotenv
from flask import Flask, jsonify

from backend.app.api import register_blueprints
from backend.app.config import config
from backend.app.extensions import bcrypt, cors, db, jwt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    os.makedirs(os.path.join(PROJECT_ROOT, 'instance'), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r'/api/*': {'origins': app.config['CORS_ORIGINS']}},
        supports_credentials=True,
    )

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    @app.get('/api/health')
    def health():
        return jsonify({'status': 'ok'})

    return app

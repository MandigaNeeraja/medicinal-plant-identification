from backend.app.api.auth import auth_bp, init_oauth
from backend.app.api.chat import chat_bp
from backend.app.api.plants import plants_bp
from backend.app.api.predictions import predictions_bp


def register_blueprints(app):
    init_oauth(app)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plants_bp, url_prefix='/api/plants')
    app.register_blueprint(predictions_bp, url_prefix='/api/predictions')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

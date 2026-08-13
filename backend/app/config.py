import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def _resolve_database_uri():
    url = os.getenv('DATABASE_URL')
    if url and url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)

    default_path = os.path.join(BASE_DIR, 'instance', 'app.db')
    if not url:
        os.makedirs(os.path.dirname(default_path), exist_ok=True)
        return f'sqlite:///{default_path}'

    if url.startswith('sqlite:///') and not url.startswith('sqlite:////'):
        relative = url.replace('sqlite:///', '', 1)
        if not os.path.isabs(relative):
            db_path = os.path.join(BASE_DIR, relative)
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            return f'sqlite:///{db_path}'

    return url


def _default_google_redirect_uri():
    api_base = os.getenv('RENDER_EXTERNAL_URL', '').rstrip('/')
    if api_base:
        return f'{api_base}/api/auth/google/callback'
    frontend = os.getenv('FRONTEND_URL', 'http://localhost:5173').rstrip('/')
    return f'{frontend}/api/auth/google/callback'


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-change-in-production')

    SQLALCHEMY_DATABASE_URI = _resolve_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1800))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800))
    )
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE', 'false').lower() == 'true'
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/api/auth/refresh'

    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', FRONTEND_URL).split(',')

    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
    GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI') or _default_google_redirect_uri()

    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.7))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'None'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

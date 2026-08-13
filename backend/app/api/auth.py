from flask import Blueprint, current_app, redirect, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from authlib.integrations.flask_client import OAuth

from backend.app.services.auth_service import AuthService
from backend.app.utils.responses import error_response, success_response

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()


def init_oauth(app):
    oauth.init_app(app)
    if AuthService.google_oauth_enabled(app.config):
        oauth.register(
            name='google',
            client_id=app.config['GOOGLE_CLIENT_ID'],
            client_secret=app.config['GOOGLE_CLIENT_SECRET'],
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'},
        )


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    try:
        user = AuthService.register(
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password'),
        )
        tokens = AuthService.create_tokens(user)
        response, status = success_response(tokens, message='Registration successful', status=201)
        response = _apply_token_cookies(response, tokens)
        return response, status
    except ValueError as exc:
        return error_response(str(exc), 400)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    try:
        user = AuthService.login(data.get('email'), data.get('password'))
        tokens = AuthService.create_tokens(user)
        response, status = success_response(tokens, message='Login successful')
        response = _apply_token_cookies(response, tokens)
        return response, status
    except ValueError as exc:
        return error_response(str(exc), 401)


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response, status = success_response(message='Logged out')
    unset_jwt_cookies(response)
    return response, status


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = AuthService.get_user_by_id(user_id)
    if not user:
        return error_response('User not found', 404)

    access_token = create_access_token(identity=str(user.id))
    response, status = success_response({'user': user.to_dict()}, message='Token refreshed')
    set_access_cookies(response, access_token)
    return response, status


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = AuthService.get_user_by_id(get_jwt_identity())
    if not user:
        return error_response('User not found', 404)
    return success_response(user.to_dict())


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user = AuthService.get_user_by_id(get_jwt_identity())
    if not user:
        return error_response('User not found', 404)

    data = request.get_json(silent=True) or {}
    try:
        updated = AuthService.update_profile(
            user,
            name=data.get('name'),
            password=data.get('password'),
        )
        return success_response(updated.to_dict(), message='Profile updated')
    except ValueError as exc:
        return error_response(str(exc), 400)


@auth_bp.route('/google/login', methods=['GET'])
def google_login():
    if not AuthService.google_oauth_enabled():
        return error_response('Google OAuth is not configured', 503)

    redirect_uri = current_app.config['GOOGLE_REDIRECT_URI']
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route('/google/callback', methods=['GET'])
def google_callback():
    if not AuthService.google_oauth_enabled():
        return error_response('Google OAuth is not configured', 503)

    token = oauth.google.authorize_access_token()
    profile = token.get('userinfo')
    if not profile:
        return error_response('Failed to fetch Google profile', 400)

    user = AuthService.upsert_google_user(profile)
    tokens = AuthService.create_tokens(user)

    frontend_url = current_app.config['FRONTEND_URL'].rstrip('/')
    response = redirect(f'{frontend_url}/dashboard')
    response = _apply_token_cookies(response, tokens)
    return response


def _apply_token_cookies(response, tokens):
    set_access_cookies(response, tokens['access_token'])
    set_refresh_cookies(response, tokens['refresh_token'])
    return response

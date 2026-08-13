import re
from datetime import datetime, timezone

from flask_jwt_extended import create_access_token, create_refresh_token

from backend.app.extensions import bcrypt, db
from backend.app.models import User

class AuthService:
    EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

    @staticmethod
    def validate_email(email):
        return bool(email and AuthService.EMAIL_PATTERN.match(email))

    @staticmethod
    def register(name, email, password):
        name = (name or '').strip()
        email = (email or '').strip().lower()
        password = password or ''

        if not name:
            raise ValueError('Name is required')
        if not AuthService.validate_email(email):
            raise ValueError('Valid email is required')
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')

        if User.query.filter_by(email=email).first():
            raise ValueError('Email is already registered')

        user = User(
            name=name,
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login(email, password):
        email = (email or '').strip().lower()
        password = password or ''

        user = User.query.filter_by(email=email).first()
        if not user or not user.password_hash:
            raise ValueError('Invalid email or password')
        if not bcrypt.check_password_hash(user.password_hash, password):
            raise ValueError('Invalid email or password')

        user.last_login = datetime.now(timezone.utc)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(int(user_id))

    @staticmethod
    def create_tokens(user):
        identity = str(user.id)
        return {
            'access_token': create_access_token(identity=identity),
            'refresh_token': create_refresh_token(identity=identity),
            'user': user.to_dict(),
        }

    @staticmethod
    def upsert_google_user(profile):
        google_id = profile.get('sub')
        email = (profile.get('email') or '').lower()
        name = profile.get('name') or email.split('@')[0]
        avatar_url = profile.get('picture')

        if not google_id or not email:
            raise ValueError('Google profile missing required fields')

        user = User.query.filter(
            (User.google_id == google_id) | (User.email == email)
        ).first()

        if user:
            user.google_id = google_id
            user.name = name or user.name
            user.avatar_url = avatar_url or user.avatar_url
        else:
            user = User(
                email=email,
                name=name,
                google_id=google_id,
                avatar_url=avatar_url,
            )
            db.session.add(user)

        user.last_login = datetime.now(timezone.utc)
        db.session.commit()
        return user

    @staticmethod
    def update_profile(user, name=None, password=None):
        if name:
            user.name = name.strip()

        if password:
            if len(password) < 8:
                raise ValueError('Password must be at least 8 characters')
            user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        db.session.commit()
        return user

    @staticmethod
    def google_oauth_enabled(app_config=None):
        if app_config is not None:
            config = app_config
        else:
            from flask import current_app
            config = current_app.config
        return bool(
            config.get('GOOGLE_CLIENT_ID')
            and config.get('GOOGLE_CLIENT_SECRET')
        )

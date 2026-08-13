from datetime import datetime, timezone

from backend.app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    google_id = db.Column(db.String(255), unique=True, nullable=True, index=True)
    avatar_url = db.Column(db.String(512), nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    last_login = db.Column(db.DateTime, nullable=True)

    predictions = db.relationship('Prediction', backref='user', lazy='dynamic')
    chat_sessions = db.relationship('ChatSession', backref='user', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'has_password': bool(self.password_hash),
        }

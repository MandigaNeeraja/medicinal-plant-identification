from datetime import datetime, timezone

from backend.app.extensions import db


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    plant_name = db.Column(db.String(120), nullable=True)
    confidence = db.Column(db.Float, nullable=False, default=0.0)
    image_path = db.Column(db.String(512), nullable=False)
    success = db.Column(db.Boolean, default=False, nullable=False)
    message = db.Column(db.String(512), nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self):
        filename = self.image_path.replace('\\', '/').split('/')[-1]
        return {
            'id': self.id,
            'plant_name': self.plant_name,
            'confidence': self.confidence,
            'image_url': f'/api/predictions/uploads/{self.user_id}/{filename}',
            'success': self.success,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

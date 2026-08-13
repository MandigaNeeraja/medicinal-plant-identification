import os
import pickle
import sys
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from backend.app.extensions import db
from backend.app.models import Prediction

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import PLANT_CLASSES, CONFIDENCE_THRESHOLD  # noqa: E402


_predictor = None


def get_predictor():
    global _predictor
    if _predictor is None:
        from src.predictor import PlantPredictor  # noqa: E402 — lazy import for Render startup

        model_dir = current_app.config['MODEL_DIR']
        _predictor = PlantPredictor(
            model_path=os.path.join(model_dir, 'best_model.h5'),
            label_encoder_path=os.path.join(model_dir, 'label_encoder.pkl'),
            preprocessing_params_path=os.path.join(model_dir, 'preprocessing_params.pkl'),
        )
    return _predictor


class PredictionService:
    @staticmethod
    def allowed_file(filename):
        return (
            '.' in filename
            and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
        )

    @staticmethod
    def user_upload_dir(user_id):
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
        os.makedirs(upload_dir, exist_ok=True)
        return upload_dir

    @staticmethod
    def predict(user_id, file):
        if not file or not file.filename:
            raise ValueError('No file provided')

        if not PredictionService.allowed_file(file.filename):
            raise ValueError('File type not allowed')

        predictor = get_predictor()
        if predictor is None:
            raise RuntimeError('Model not loaded')

        original_name = secure_filename(file.filename)
        unique_name = f'{uuid.uuid4().hex}_{original_name}'
        upload_dir = PredictionService.user_upload_dir(user_id)
        filepath = os.path.join(upload_dir, unique_name)
        file.save(filepath)

        threshold = current_app.config.get('CONFIDENCE_THRESHOLD', CONFIDENCE_THRESHOLD)
        result = predictor.predict(filepath, confidence_threshold=threshold)

        plant_name = result.get('plant')
        if result.get('success') and plant_name in PLANT_CLASSES:
            result['medicinal_uses'] = PLANT_CLASSES[plant_name]['medicinal_uses']

        result['image_url'] = f'/api/predictions/uploads/{user_id}/{unique_name}'

        record = Prediction(
            user_id=user_id,
            plant_name=plant_name,
            confidence=result.get('confidence', 0.0),
            image_path=filepath,
            success=bool(result.get('success')),
            message=result.get('message'),
        )
        db.session.add(record)
        db.session.commit()
        result['prediction_id'] = record.id
        return result

    @staticmethod
    def get_history(user_id, page=1, per_page=10):
        query = Prediction.query.filter_by(user_id=user_id).order_by(Prediction.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': [item.to_dict() for item in pagination.items],
            'page': pagination.page,
            'pages': pagination.pages,
            'total': pagination.total,
        }

    @staticmethod
    def get_recent(user_id, limit=5):
        items = (
            Prediction.query.filter_by(user_id=user_id)
            .order_by(Prediction.created_at.desc())
            .limit(limit)
            .all()
        )
        return [item.to_dict() for item in items]

    @staticmethod
    def get_model_info():
        model_dir = current_app.config['MODEL_DIR']
        info_path = os.path.join(model_dir, 'model_info.pkl')
        with open(info_path, 'rb') as handle:
            return pickle.load(handle)

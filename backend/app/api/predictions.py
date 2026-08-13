import os

from flask import Blueprint, request, send_from_directory
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.app.services.prediction_service import PredictionService
from backend.app.utils.responses import error_response, success_response

predictions_bp = Blueprint('predictions', __name__)


@predictions_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    user_id = int(get_jwt_identity())
    file = request.files.get('file')

    try:
        result = PredictionService.predict(user_id, file)
        return success_response(result)
    except ValueError as exc:
        return error_response(str(exc), 400)
    except RuntimeError as exc:
        return error_response(str(exc), 500)
    except Exception as exc:
        return error_response(f'Prediction failed: {exc}', 500)


@predictions_bp.route('/history', methods=['GET'])
@jwt_required()
def history():
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    data = PredictionService.get_history(user_id, page=page, per_page=per_page)
    return success_response(data)


@predictions_bp.route('/recent', methods=['GET'])
@jwt_required()
def recent():
    user_id = int(get_jwt_identity())
    limit = request.args.get('limit', 5, type=int)
    return success_response(PredictionService.get_recent(user_id, limit=limit))


@predictions_bp.route('/model-info', methods=['GET'])
@jwt_required()
def model_info():
    try:
        return success_response(PredictionService.get_model_info())
    except Exception as exc:
        return error_response(f'Could not load model info: {exc}', 500)


@predictions_bp.route('/uploads/<int:user_id>/<path:filename>', methods=['GET'])
@jwt_required()
def uploaded_file(user_id, filename):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return error_response('Forbidden', 403)

    upload_dir = PredictionService.user_upload_dir(user_id)
    file_path = os.path.join(upload_dir, filename)
    if not os.path.exists(file_path):
        return error_response('File not found', 404)

    return send_from_directory(upload_dir, filename)

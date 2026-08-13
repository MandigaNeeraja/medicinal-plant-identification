from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.app.services.chat_service import ChatService
from backend.app.utils.responses import error_response, success_response

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/init', methods=['POST'])
@jwt_required()
def init_chat():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    plant_name = (data.get('plant_name') or '').strip()

    if not plant_name:
        return error_response('plant_name is required', 400)

    try:
        result = ChatService.init_chat(user_id, plant_name)
        return success_response(result)
    except Exception as exc:
        return error_response(str(exc), 400)


@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def chat_message():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    plant_name = (data.get('plant_name') or '').strip()
    message = (data.get('message') or '').strip()

    if not plant_name:
        return error_response('plant_name is required', 400)

    try:
        result = ChatService.send_message(user_id, plant_name, message)
        return success_response(result)
    except ValueError as exc:
        return error_response(str(exc), 400)
    except Exception as exc:
        return error_response(str(exc), 500)


@chat_bp.route('/history/<plant_name>', methods=['GET'])
@jwt_required()
def chat_history(plant_name):
    user_id = int(get_jwt_identity())
    result = ChatService.get_history(user_id, plant_name)
    return success_response(result)

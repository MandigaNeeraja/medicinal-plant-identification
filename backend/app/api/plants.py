from flask import Blueprint, send_file
from flask_jwt_extended import jwt_required

from backend.app.services.plant_service import PlantService
from backend.app.utils.responses import error_response, success_response

plants_bp = Blueprint('plants', __name__)


@plants_bp.route('', methods=['GET'])
@jwt_required()
def list_plants():
    return success_response(PlantService.list_plants())


@plants_bp.route('/<plant_name>', methods=['GET'])
@jwt_required()
def get_plant(plant_name):
    plant = PlantService.get_plant(plant_name)
    if not plant:
        return error_response('Plant not found', 404)
    return success_response(plant)


@plants_bp.route('/images/<path:image_filename>', methods=['GET'])
@jwt_required()
def plant_image(image_filename):
    image_path = PlantService.plant_image_path(image_filename)
    if not image_path:
        return error_response('Image not found', 404)
    return send_file(image_path)
